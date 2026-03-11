import { countries, getCountryMultiplier } from './country-data.js';

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

function level(score) {
  if (score < 35) return 'Low';
  if (score < 70) return 'Moderate';
  return 'High';
}

export function initPracticalDatingCalculator({ toolName, weight = 1 }) {
  const countryEl = document.querySelector('#country');
  const ageEl = document.querySelector('#age');
  const incomeEl = document.querySelector('#income');
  const preferenceEl = document.querySelector('#preference');
  const consistencyEl = document.querySelector('#consistency');
  const btn = document.querySelector('#calculateBtn');
  const resultEl = document.querySelector('#result');

  countryEl.innerHTML = countries.map((c) => `<option value="${c.value}">${c.label}</option>`).join('');

  function score() {
    const countryFactor = getCountryMultiplier(countryEl.value);
    const ageFactor = clamp((Number(ageEl.value) - 18) / 50, 0, 1);
    const incomeFactor = clamp(Number(incomeEl.value) / 220000, 0, 1);
    const prefFactor = clamp(Number(preferenceEl.value) / 10, 0, 1);
    const consistencyFactor = clamp(Number(consistencyEl.value) / 10, 0, 1);

    const base = (incomeFactor * 0.30) + (prefFactor * 0.30) + (consistencyFactor * 0.28) + ((1 - ageFactor) * 0.12);
    const out = clamp(base * 100 * countryFactor * weight, 0, 100);
    return out;
  }

  function render() {
    const s = score();
    resultEl.innerHTML = `
      <article class="result-card">
        <h3>${toolName} Result</h3>
        <p><strong>Country:</strong> ${countryEl.options[countryEl.selectedIndex].text}</p>
        <p><strong>Score:</strong> ${s.toFixed(1)}%</p>
        <p><strong>Level:</strong> ${level(s)}</p>
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
