export function calculateCompetitionRatio(targetMalePercentage, femalePopulation, malePopulation) {
  const eligibleMen = Math.max(1, malePopulation * targetMalePercentage);
  const ratio = femalePopulation / eligibleMen;
  return {
    eligible_men: Math.round(eligibleMen),
    ratio,
    label: `1 man : ${Math.max(1, Math.round(ratio))} women`
  };
}
