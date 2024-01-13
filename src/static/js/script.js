let currentStep = 1;
const form = document.getElementById('bookingForm');

function showStep(step) {
  const steps = document.querySelectorAll('.wizard-step');
  steps.forEach(s => s.classList.add("d-none"));

  const currentStepElement = document.querySelector(`.wizard-step[data-step="${step}"]`);
  if (currentStepElement) {
    currentStepElement.classList.remove("d-none");
  }
}

function nextStep(step) {
  currentStep += step;
  showStep(currentStep);
}

function prevStep(step) {
  currentStep -= step;
  showStep(currentStep);
}

// Toon het eerste stapformulier bij het laden van de pagina
showStep(currentStep);
