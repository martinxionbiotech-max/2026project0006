import { countries, getCountryMultiplier } from './country-data.js';

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

export function initCompatibilityCalculator({ toolName, weight = 1 }) {
  const countryEl = document.querySelector('#country');
  const ageGapEl = document.querySelector('#ageGap');
  const lifestyleEl = document.querySelector('#lifestyle');
  const communicationEl = document.querySelector('#communication');
  const valuesEl = document.querySelector('#values');
  const calculateBtn = document.querySelector('#calculateBtn');
  const shareBtn = document.querySelector('#shareBtn');
  const resultEl = document.querySelector('#result');

  countryEl.innerHTML = countries.map((c) => `<option value="${c.value}">${c.label}</option>`).join('');

  function computeScore() {
    const countryFactor = getCountryMultiplier(countryEl.value);
    const ageGapPenalty = clamp(Number(ageGapEl.value) / 20, 0, 1);
    const lifestyleScore = clamp(Number(lifestyleEl.value) / 10, 0, 1);
    const communicationScore = clamp(Number(communicationEl.value) / 10, 0, 1);
    const valuesScore = clamp(Number(valuesEl.value) / 10, 0, 1);

    const base = (lifestyleScore * 0.32) + (communicationScore * 0.36) + (valuesScore * 0.32);
    const adjusted = (base * (1 - ageGapPenalty * 0.35)) * countryFactor * weight;
    return clamp(adjusted * 100, 0, 100);
  }

  function render() {
    const score = computeScore();
    resultEl.innerHTML = `
      <article class="result-card">
        <h3>${toolName} Result</h3>
        <p><strong>Country:</strong> ${countryEl.options[countryEl.selectedIndex].text}</p>
        <p><strong>Compatibility Score:</strong> ${score.toFixed(1)}%</p>
      </article>
    `;
    return score;
  }

  calculateBtn.addEventListener('click', () => {
    calculateBtn.classList.add('is-generating');
    calculateBtn.textContent = 'Calculating...';
    render();
    setTimeout(() => {
      calculateBtn.classList.remove('is-generating');
      calculateBtn.textContent = 'Calculate Compatibility';
    }, 260);
  });

  shareBtn.addEventListener('click', () => {
    const score = render().toFixed(1);
    const text = encodeURIComponent(`${toolName}: ${score}% compatibility score`);
    window.open(`https://twitter.com/intent/tweet?text=${text}`, '_blank');
  });

  render();
}
