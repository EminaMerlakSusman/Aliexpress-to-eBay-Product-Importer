function updateProgress(progressBarElement, progressBarMessageElement, progress) {
  progressBarElement.style.width = progress.percent + "%";
  progressBarMessageElement.innerHTML = progress.current + ' of ' + progress.total + ' processed.';
}

var trigger = document.getElementById('post-url');
trigger.addEventListener('click', function(e) {
  var bar = document.getElementById("post-url");
  var barMessage = document.getElementById("progress-bar-message");
  for (var i = 0; i < 11; i++) {
    setTimeout(updateProgress, 500 * i, bar, barMessage, {
      percent: 10 * i,
      current: 10 * i,
      total: 100
    })
  }
})

function updateProgress (progressUrl) {
    fetch(progressUrl).then(function(response) {
        response.json().then(function(data) {
            // update the appropriate UI components
            setProgress(data.state, data.details);
            setTimeout(updateProgress, 500, progressUrl);
        });
    });
}
var progressUrl = '{% url "task_status" task_id %}';  // django template usage
updateProgress(progressUrl);