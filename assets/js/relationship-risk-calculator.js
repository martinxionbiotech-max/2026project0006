import { countries, getCountryMultiplier } from './country-data.js';

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

function riskLabel(score) {
  if (score < 35) return 'Low Risk';
  if (score < 68) return 'Moderate Risk';
  return 'High Risk';
}

export function initRelationshipRiskTool({ toolName, baseline = 50 }) {
  const countryEl = document.querySelector('#country');
  const ageEl = document.querySelector('#age');
  const heightEl = document.querySelector('#height');
  const incomeEl = document.querySelector('#income');
  const educationEl = document.querySelector('#education');
  const btn = document.querySelector('#calculateBtn');
  const result = document.querySelector('#result');

  countryEl.innerHTML = countries.map((c) => `<option value="${c.value}">${c.label}</option>`).join('');

  function calculate() {
    const countryFactor = 1 + (1 - getCountryMultiplier(countryEl.value)) * 0.35;
    const ageFactor = clamp((Number(ageEl.value) - 18) / 50, 0, 1);
    const heightFactor = 1 - clamp((Number(heightEl.value) - 150) / 70, 0, 1);
    const incomeFactor = 1 - clamp(Number(incomeEl.value) / 220000, 0, 1);
    const educationFactor = 1 - clamp(Number(educationEl.value) / 10, 0, 1);

    const score = clamp((baseline * 0.35) + (ageFactor * 20) + (heightFactor * 10) + (incomeFactor * 20) + (educationFactor * 15), 1, 99) * countryFactor;
    const normalized = clamp(score, 1, 99);
    return { score: normalized, label: riskLabel(normalized) };
  }

  function render() {
    const { score, label } = calculate();
    result.innerHTML = `
      <article class="result-card">
        <h3>${toolName} Score</h3>
        <p><strong>Country:</strong> ${countryEl.options[countryEl.selectedIndex].text}</p>
        <p><strong>Risk Score:</strong> ${score.toFixed(1)}/100</p>
        <p><strong>Result:</strong> ${label}</p>
      </article>
    `;
  }

  btn.addEventListener('click', () => {
    btn.classList.add('is-generating');
    btn.textContent = 'Calculating...';
    render();
    setTimeout(() => {
      btn.classList.remove('is-generating');
      btn.textContent = 'Calculate';
    }, 260);
  });

  render();
}
