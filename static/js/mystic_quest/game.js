window.addEventListener("load", startGame);

async function startGame() {
  const response = await fetch("/api/game/start", {
    method: "POST",
  });

  const result = await response.json();

  loadQuestion(result);
}

const state = {
  totalLives: 3,
  currentLives: 3,
  progress: 0,
  currentQuestion: 1,
  remainingAttempts: 3

};

// Elementos del dom
const answerInput = document.getElementById("answer");
const continueBtn = document.getElementById("continue-btn");
const heartContainer = document.getElementById("heart-container");
const attemptContainer = document.getElementById("attempt-container");
const progressBar = document.getElementById("progress-bar");
const progressText = document.getElementById("progress-percent");

// Inicializa la interfaz con el estado inicial
function init() {
  updateHearts();
  updateAttempts();
  updateProgress();
}

function updateHearts() {
  const hearts = heartContainer.querySelectorAll(".heart");
  hearts.forEach((heart, index) => {
    if (index < state.currentLives) {
      heart.classList.add("filled");
      heart.classList.remove("lost");
    } else {
      heart.classList.remove("filled");
      heart.classList.add("lost");
    }
  });
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

  const response = await fetch("/api/game/answer", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      answer: answer,
    }),
  });

  const result = await response.json();

  console.log(result);
}

function updateProgress() {
  progressBar.style.width = `${state.progress}%`;
  progressText.textContent = `${state.progress}%`;
}


function handleLifeLoss() {
  if (state.currentLives > 0) {
    state.currentLives--;
    updateHearts();
    if (state.currentLives === 0) {
      alert("¡Juego Terminado! Te has quedado sin vidas.");
      location.reload();
    } else {
      alert("Has perdido una vida. Los intentos se reinician.");
      state.remainingAttempts = 3;
      updateAttempts();
    }
  }
}

// Event Listeners
continueBtn.addEventListener("click", handleSubmission);

answerInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    handleSubmission();
  }
});

function loadQuestion(data) {
  document.querySelector(".hint-text").textContent = data.hint;

  //document.querySelector(".game-image").src = data.image;

  state.currentLives = data.lives;

  state.progress = state.currentQuestion === 1 ? 0 : ((state.currentQuestion - 1) / 5) * 100;

  updateHearts();

  updateProgress();
}
// Run Init
init();
