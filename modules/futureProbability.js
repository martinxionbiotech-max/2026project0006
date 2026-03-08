export function calculateFutureDatingProbability({ age, dating_pool_size, city_population, marriage_rate }) {
  const years = Math.max(1, 40 - age);
  const matchProbability = Math.min(0.95, Math.max(0.0001, dating_pool_size / Math.max(1, city_population)));
  const probability = 1 - ((1 - (matchProbability * marriage_rate)) ** years);

  return {
    years,
    probability,
    label: `${Math.round(probability * 100)}%`
  };
}
