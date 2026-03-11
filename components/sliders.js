export function renderSliders(container, onChange, initialState) {
  container.innerHTML = `
    <h3>Reality Adjustment Simulator</h3>
    <label>Height Slider (cm): <strong id="heightSliderValue">${initialState.height}</strong>
      <input id="heightSlider" type="range" min="170" max="195" value="${initialState.height}" />
    </label>
    <label>Income Slider (USD): <strong id="incomeSliderValue">${initialState.income.toLocaleString()}</strong>
      <input id="incomeSlider" type="range" min="30000" max="200000" step="5000" value="${initialState.income}" />
    </label>
    <label>Age Range Slider (max age): <strong id="ageRangeSliderValue">${initialState.ageMax}</strong>
      <input id="ageRangeSlider" type="range" min="24" max="45" value="${initialState.ageMax}" />
    </label>
  `;

  const emit = () => {
    const next = {
      height: Number(container.querySelector('#heightSlider').value),
      income: Number(container.querySelector('#incomeSlider').value),
      ageMax: Number(container.querySelector('#ageRangeSlider').value)
    };

    container.querySelector('#heightSliderValue').textContent = String(next.height);
    container.querySelector('#incomeSliderValue').textContent = next.income.toLocaleString();
    container.querySelector('#ageRangeSliderValue').textContent = String(next.ageMax);
    onChange(next);
  };

  ['heightSlider', 'incomeSlider', 'ageRangeSlider'].forEach((id) => {
    container.querySelector(`#${id}`).addEventListener('input', emit);
  });
}
