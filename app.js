import { getPopulationData } from './dataset.js';
import { buildRealityReport } from './calculator.js';
import { renderResultCard } from './components/resultCard.js';
import { renderPoolChart } from './components/charts.js';
import { renderSliders } from './components/sliders.js';

let allData;
let sliderState = { height: 180, income: 100000, ageMax: 35 };

const resultCard = document.querySelector('#resultCard');
const chartCanvas = document.querySelector('#poolChart');

function syncManualInputsWithSliders() {
  document.querySelector('#heightMin').value = String(sliderState.height);
  document.querySelector('#incomeMin').value = String(sliderState.income);
  document.querySelector('#ageMax').value = String(sliderState.ageMax);
}

function collectInputs() {
  return {
    poolInput: {
      gender_target: document.querySelector('#genderTarget').value,
      age_min: Number(document.querySelector('#ageMin').value),
      age_max: sliderState.ageMax,
      height_min: sliderState.height,
      income_min: sliderState.income,
      marital_status: document.querySelector('#maritalStatus').value,
      bmi_range: document.querySelector('#bmiRange').value,
      country: document.querySelector('#country').value
    },
    marketInput: {
      age: Number(document.querySelector('#userAge').value),
      height: Number(document.querySelector('#userHeight').value),
      income: Number(document.querySelector('#userIncome').value),
      fitness: Number(document.querySelector('#fitness').value),
      face_score: Number(document.querySelector('#faceScore').value),
      education: Number(document.querySelector('#education').value),
      confidence: Number(document.querySelector('#confidence').value),
      social_skills: Number(document.querySelector('#socialSkills').value)
    }
  };
}

function generateReport() {
  const country = document.querySelector('#country').value;
  const inputs = collectInputs();
  const report = buildRealityReport(inputs, allData[country]);
  renderResultCard(resultCard, report);
  renderPoolChart(chartCanvas, report.simulator);
}

function bindShareActions() {
  document.querySelector('#shareTwitter').addEventListener('click', () => {
    const text = encodeURIComponent(`My Dating Reality Report: ${resultCard.innerText.replace(/\s+/g, ' ').trim()} ${window.location.href}`);
    window.open(`https://twitter.com/intent/tweet?text=${text}`, '_blank');
  });

  document.querySelector('#copyLink').addEventListener('click', async () => {
    await navigator.clipboard.writeText(window.location.href);
  });

  document.querySelector('#downloadImage').addEventListener('click', () => {
    const blob = new Blob([resultCard.innerHTML], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'dating-reality-result.html';
    a.click();
    URL.revokeObjectURL(url);
  });
}

function bindManualPoolInputs() {
  const ageMaxInput = document.querySelector('#ageMax');
  const heightInput = document.querySelector('#heightMin');
  const incomeInput = document.querySelector('#incomeMin');

  ageMaxInput.addEventListener('change', () => {
    sliderState.ageMax = Number(ageMaxInput.value);
    generateReport();
  });
  heightInput.addEventListener('change', () => {
    sliderState.height = Number(heightInput.value);
    generateReport();
  });
  incomeInput.addEventListener('change', () => {
    sliderState.income = Number(incomeInput.value);
    generateReport();
  });
}

async function main() {
  allData = await getPopulationData();
  bindManualPoolInputs();
  renderSliders(document.querySelector('#sliderContainer'), (nextState) => {
    sliderState = nextState;
    syncManualInputsWithSliders();
    generateReport();
  }, sliderState);
  bindShareActions();
  document.querySelector('#generateBtn').addEventListener('click', generateReport);
  syncManualInputsWithSliders();
  generateReport();
}

main();
