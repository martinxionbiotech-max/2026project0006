function ageBucketRate(ageMin, ageMax, ageDistribution) {
  if (ageMin >= 25 && ageMax <= 35) return ageDistribution['25-35'] ?? 0.18;
  if (ageMin >= 18 && ageMax <= 24) return ageDistribution['18-24'] ?? 0.12;
  return ageDistribution['36-45'] ?? 0.16;
}

function heightRate(heightMin, data) {
  if (heightMin >= 185) return data.height_over_185;
  if (heightMin >= 180) return data.height_over_180;
  return data.height_over_175;
}

function incomeRate(incomeMin, data) {
  if (incomeMin >= 150000) return data.income_over_150000;
  if (incomeMin >= 100000) return data.income_over_100000;
  return data.income_over_50000;
}

export function calculateDatingPool(input, data) {
  const ageP = ageBucketRate(input.age_min, input.age_max, data.age_distribution);
  const heightP = heightRate(input.height_min, data);
  const incomeP = incomeRate(input.income_min, data);
  const singleP = data.single_rate;
  const bmiP = data.non_obese;

  const percentage = ageP * heightP * incomeP * singleP * bmiP;
  const relevantPopulation = input.gender_target === 'male' ? data.male_population : data.female_population;

  return {
    percentage,
    matching_population: Math.round(relevantPopulation * percentage),
    total_population: relevantPopulation
  };
}
