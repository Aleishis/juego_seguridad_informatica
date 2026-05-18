window.addEventListener("load", startGame);

async function startGame() {
  const response = await fetch("/api/game/start", {
    method: "POST",
  });

  const result = await response.json();

  loadQuestion(result);
}

const state = {
  progress: 0,
  currentQuestion: 1,
  remainingAttempts: 3,
  score: 0
};

// Elementos del dom
const answerInput = document.getElementById("answer");
const continueBtn = document.getElementById("btn-continue");
const heartContainer = document.getElementById("heart-container");
const attemptContainer = document.getElementById("attempt-container");
const progressBar = document.getElementById("progress-bar");
const progressText = document.getElementById("progress-percent");

// Inicializa la interfaz con el estado inicial
function init() {
  updateAttempts();
  updateProgress();
}


function updateAttempts() {
  const dots = attemptContainer.querySelectorAll(".attempt-dot");
  dots.forEach((dot, index) => {
    if (index < state.remainingAttempts) {
      dot.classList.remove("used");
    } else {
      dot.classList.add("used");
    }
  });
}

async function handleSubmission() {
  const answer = answerInput.value.trim();

  if (!answer) return;

  fetch("/api/game/answer", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({answer: answer})
  }).then (response => response.json())
  .then(result => {
    if(result.correct){

      state.score += 1;

      if (state.score >= 5){
        alert("¡Felicidades! Has completado el juego con éxito.");
        window.location.href = "/welcome";
        return;
      }
      alert("¡Respuesta Correcta!");
      state.currentQuestion++;
      document.getElementById("current-level").textContent = state.currentQuestion;
      updateAttempts();
      loadQuestion(result);
    }
    else {
      state.remainingAttempts--;
      handleLifeLoss();
      updateAttempts();
    }
  });

}

function updateProgress() {
  progressBar.style.width = `${state.progress}%`;
  progressText.textContent = `${state.progress}%`;
}


function handleLifeLoss() {
  if (state.remainingAttempts <= 0) {
    alert("¡Has perdido todas tus vidas!");
    window.location.href = "/welcome";
  } else {
    alert(`Respuesta Incorrecta. Te quedan ${state.remainingAttempts} intentos.`);
  }
}

continueBtn.addEventListener("click", handleSubmission);

answerInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    handleSubmission();
  }
});

function loadQuestion(data) {
  document.querySelector(".hint-text").textContent = data.hint;

  //document.querySelector(".game-image").src = data.image;

  state.progress = state.currentQuestion === 1 ? 0 : ((state.currentQuestion - 1) / 5) * 100;

  updateProgress();
}
// Run Init
init();
