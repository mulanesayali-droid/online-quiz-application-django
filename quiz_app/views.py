from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Attempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Avg, Max, Count



from django.contrib.auth import logout
def leaderboard(request):
    leaderboard_data = (
        Attempt.objects
        .values("user__username", "quiz__title")
        .annotate(best_score=Max("score"))
        .order_by("-best_score")
    )

    return render(request, "quiz_app/leaderboard.html", {
        "leaderboard": leaderboard_data
    })
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})
def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_app/home.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()

    if request.method == "POST":
        score = 0
        total = questions.count()

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected and int(selected) == question.correct_option:
                score += 1

        Attempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total=total
        )

        return render(request, 'quiz_app/result.html', {
            'quiz': quiz,
            'score': score,
            'total': total
        })

    return render(request, 'quiz_app/take_quiz.html', {
        'quiz': quiz,
        'questions': questions
    })
@login_required
def results(request):
    attempts = Attempt.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'quiz_app/results.html', {'attempts': attempts})

@login_required
def analytics_dashboard(request):
    total_quizzes = Quiz.objects.count()
    total_attempts = Attempt.objects.count()

    avg_score = Attempt.objects.aggregate(avg=Avg('score'))['avg'] or 0
    best_score = Attempt.objects.aggregate(max=Max('score'))['max'] or 0

    attempts_per_quiz = (
        Attempt.objects
        .values('quiz__title')
        .annotate(attempts=Count('id'))
        .order_by('-attempts')
    )

    user_stats = (
        Attempt.objects
        .filter(user=request.user)
        .aggregate(
            avg=Avg('score'),
            best=Max('score'),
            total=Count('id')
        )
    )

    return render(request, 'quiz_app/analytics.html', {
        'total_quizzes': total_quizzes,
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 2),
        'best_score': best_score,
        'attempts_per_quiz': attempts_per_quiz,
        'user_stats': user_stats
    })
