let currentStep = 1;

function showStep(step) {
  // show form step
  document.querySelectorAll('.step').forEach(s => s.classList.add('hidden'));
  document.querySelector(`.step[data-step="${step}"]`).classList.remove('hidden');

  // update vertical stepper
  document.querySelectorAll('.stepper-item').forEach(item => {
    item.classList.remove('active');
    if (Number(item.dataset.step) === step) {
      item.classList.add('active');
    }
  });

  currentStep = step;
}

function nextStep() {
  const current = document.querySelector(`.step[data-step="${currentStep}"]`);
  const inputs = current.querySelectorAll('input, select, textarea');

  for (let input of inputs) {
    if (!input.checkValidity()) {
      input.reportValidity();
      return;
    }
  }

  showStep(currentStep + 1);
}

function prevStep() {
  showStep(currentStep - 1);
}

function updateTriageColor(value) {
  const box = document.getElementById('triageColor');
  const colors = {
    Red: '#ef4444',
    Yellow: '#facc15',
    Green: '#22c55e',
    White: '#e5e7eb',
    Black: '#000000'
  };
  box.style.backgroundColor = colors[value] || '#d1d5db';
}

// Run AFTER page loads
document.addEventListener('DOMContentLoaded', () => {
  showStep(1);
});

document.addEventListener("DOMContentLoaded", () => {
  showPage("dashboard", document.querySelector(".nav-btn"));
});