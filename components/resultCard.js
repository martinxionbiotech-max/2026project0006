function pct(value) {
  return `${(value * 100).toFixed(2)}%`;
}

export function renderResultCard(container, report) {
  container.innerHTML = `
    <article class="result-card" id="resultCapture">
      <h3>Dating Reality Report</h3>
      <p><strong>Dating pool:</strong> ${pct(report.datingPool.percentage)} (${report.datingPool.matching_population.toLocaleString()} matches)</p>
      <p><strong>Your value:</strong> ${report.marketValue.score}/10 (${report.marketValue.category}, approx. ${report.marketValue.percentile}th percentile)</p>
      <p><strong>Competition:</strong> ${report.competition.label}</p>
      <p><strong>Marriage probability by 40:</strong> ${report.future.label}</p>

      <div class="metric-notes">
        <h4>Metric Notes</h4>
        <ul>
          <li>Dating pool = age rate × height rate × income rate × single rate × non-obese rate.</li>
          <li>Competition ratio compares female population to eligible men pool size.</li>
          <li>Future probability compounds annual matching chance up to age 40.</li>
        </ul>
      </div>
    </article>
  `;
}
