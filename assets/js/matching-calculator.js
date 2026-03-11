import { countries, getCountryMultiplier } from './country-data.js';

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

export function initMatchingCalculator({ toolName, strictness = 1 }) {
  const countryEl = document.querySelector('#country');
  const ageEl = document.querySelector('#age');
  const heightEl = document.querySelector('#height');
  const incomeEl = document.querySelector('#income');
  const educationEl = document.querySelector('#education');
  const btn = document.querySelector('#calculateBtn');
  const result = document.querySelector('#result');

  countryEl.innerHTML = countries
    .map((c) => `<option value="${c.value}">${c.label}</option>`)
    .join('');

  function calculatePercentage() {
    const countryFactor = getCountryMultiplier(countryEl.value);
    const agePenalty = clamp((Number(ageEl.value) - 22) / 30, 0, 1);
    const heightPenalty = clamp((Number(heightEl.value) - 165) / 35, 0, 1);
    const incomePenalty = clamp(Number(incomeEl.value) / 200000, 0, 1);
    const educationPenalty = clamp(Number(educationEl.value) / 10, 0, 1);

    const score = (agePenalty * 0.22) + (heightPenalty * 0.26) + (incomePenalty * 0.32) + (educationPenalty * 0.20);
    const percentage = clamp((1 - score * strictness) * 100 * countryFactor, 0.01, 85);
    return percentage;
  }

  function render() {
    const percentage = calculatePercentage();
    result.innerHTML = `
      <article class="result-card">
        <h3>${toolName} Result</h3>
        <p><strong>Country:</strong> ${countryEl.options[countryEl.selectedIndex].text}</p>
        <p><strong>Matching population percentage:</strong> ${percentage.toFixed(2)}%</p>
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
