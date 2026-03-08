function normalizeIncome(income) {
  if (income >= 150000) return 10;
  if (income >= 100000) return 8;
  if (income >= 50000) return 6;
  return 4;
}

function percentileFromScore(score) {
  return Math.min(99, Math.max(1, Math.round(score * 10 + 10)));
}

function category(score) {
  if (score >= 8) return 'Elite Value';
  if (score >= 6.5) return 'High Value';
  if (score >= 5) return 'Average';
  return 'Needs Improvement';
}

export function calculateMarketValue(input) {
  const physicalScore = (input.fitness + input.face_score + Math.min(10, input.height / 20)) / 3;
  const statusScore = (normalizeIncome(input.income) + input.education) / 2;
  const personalityScore = (input.confidence + input.social_skills) / 2;

  const score = (physicalScore * 0.5) + (statusScore * 0.3) + (personalityScore * 0.2);

  return {
    score: Number(score.toFixed(1)),
    percentile: percentileFromScore(score),
    category: category(score)
  };
}
