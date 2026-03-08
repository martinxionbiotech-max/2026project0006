import { countries, getCountryMultiplier } from './country-data.js';

export function mountCountrySelector(selectEl) {
  selectEl.innerHTML = countries
    .map((c) => `<option value="${c.value}">${c.label}</option>`)
    .join('');
}

export function initTemplateCalculator({ toolName, baseValue }) {
  const country = document.querySelector('#country');
  const inputA = document.querySelector('#inputA');
  const inputB = document.querySelector('#inputB');
  const btn = document.querySelector('#calculateBtn');
  const result = document.querySelector('#result');

  mountCountrySelector(country);

  function run() {
    const factor = getCountryMultiplier(country.value);
    const value = (Number(inputA.value) + Number(inputB.value)) * factor * baseValue;
    result.innerHTML = `
      <article class="result-card">
        <h3>${toolName} Result</h3>
        <p><strong>Country:</strong> ${country.options[country.selectedIndex].text}</p>
        <p><strong>Score:</strong> ${value.toFixed(2)}</p>
      </article>
    `;
  }

  btn.addEventListener('click', () => {
    btn.classList.add('is-generating');
    btn.textContent = 'Calculating...';
    run();
    setTimeout(() => {
      btn.classList.remove('is-generating');
      btn.textContent = 'Calculate';
    }, 260);
  });

  run();
}
