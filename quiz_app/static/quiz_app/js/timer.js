function startTimer(duration, formId) {
    let timer = duration, minutes, seconds;
    const display = document.getElementById('timer');
    const interval = setInterval(function () {
        minutes = parseInt(timer / 60);
        seconds = parseInt(timer % 60);
        display.textContent = minutes + ":" + (seconds < 10 ? "0" : "") + seconds;

        if (--timer < 0) {
            clearInterval(interval);
            alert("Time is up! Submitting quiz...");
            document.getElementById(formId).submit();
        }
    }, 1000);
}
