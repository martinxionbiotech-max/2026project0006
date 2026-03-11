import { countries, getCountryMultiplier } from './country-data.js';

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

function vibeLabel(score) {
  if (score < 30) return '🧊 Hidden Gem';
  if (score < 55) return '😌 Solid Potential';
  if (score < 75) return '🔥 Viral Energy';
  return '🚀 Main Character Mode';
}

export function initViralDatingCalculator({ toolName, bias = 1 }) {
  const countryEl = document.querySelector('#country');
  const confidenceEl = document.querySelector('#confidence');
  const socialEl = document.querySelector('#social');
  const consistencyEl = document.querySelector('#consistency');
  const effortEl = document.querySelector('#effort');
  const btn = document.querySelector('#calculateBtn');
  const resultEl = document.querySelector('#result');

  countryEl.innerHTML = countries.map((c) => `<option value="${c.value}">${c.label}</option>`).join('');

  function calc() {
    const countryFactor = getCountryMultiplier(countryEl.value);
    const confidence = clamp(Number(confidenceEl.value) / 10, 0, 1);
    const social = clamp(Number(socialEl.value) / 10, 0, 1);
    const consistency = clamp(Number(consistencyEl.value) / 10, 0, 1);
    const effort = clamp(Number(effortEl.value) / 10, 0, 1);

    const score = clamp(((confidence * 0.32) + (social * 0.24) + (consistency * 0.20) + (effort * 0.24)) * 100 * countryFactor * bias, 0, 100);
    return score;
  }

  function render() {
    const score = calc();
    const label = vibeLabel(score);
    const rarity = (100 - score).toFixed(1);

    resultEl.innerHTML = `
      <article class="result-card">
        <h3>${toolName} Result</h3>
        <p><strong>Country:</strong> ${countryEl.options[countryEl.selectedIndex].text}</p>
        <p><strong>Viral Score:</strong> ${score.toFixed(1)}%</p>
        <p><strong>Status:</strong> ${label}</p>
        <p><strong>Rarity Meter:</strong> Top ${rarity}% vibe bracket</p>
      </article>
    `;
  }

  btn.addEventListener('click', () => {
    btn.classList.add('is-generating');
    btn.textContent = 'Analyzing...';
    render();
    setTimeout(() => {
      btn.classList.remove('is-generating');
      btn.textContent = 'Generate Viral Score';
    }, 260);
  });

  render();
}
