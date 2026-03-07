let chart;

export function renderPoolChart(canvas, simulatorData) {
  const labels = simulatorData.map((s) => `≥${s.height}cm`);
  const values = simulatorData.map((s) => Number((s.percentage * 100).toFixed(2)));

  if (chart) {
    chart.data.labels = labels;
    chart.data.datasets[0].data = values;
    chart.update();
    return;
  }

  chart = new Chart(canvas.getContext('2d'), {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Dating pool %',
        data: values,
        backgroundColor: '#7b5cff'
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}
