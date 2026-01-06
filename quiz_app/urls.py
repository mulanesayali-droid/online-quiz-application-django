from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('results/', views.results, name='results'),
    path('accounts/register/', views.register, name='signup'),

    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('analytics/', views.analytics_dashboard, name='analytics'),


]
