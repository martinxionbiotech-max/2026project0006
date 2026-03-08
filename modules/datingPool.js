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

function maritalRate(maritalStatus, data) {
  if (maritalStatus === 'married') return data.married_rate ?? 0.45;
  if (maritalStatus === 'divorced') return data.divorced_rate ?? 0.15;
  return data.single_rate ?? 0.4;
}

function bmiRate(bmiRange, data) {
  if (bmiRange === 'overweight') return data.overweight ?? 0.28;
  if (bmiRange === 'obese') return data.obese ?? 0.12;
  return data.non_obese ?? 0.6;
}

export function calculateDatingPool(input, data) {
  const ageP = ageBucketRate(input.age_min, input.age_max, data.age_distribution);
  const heightP = heightRate(input.height_min, data);
  const incomeP = incomeRate(input.income_min, data);
  const maritalP = maritalRate(input.marital_status, data);
  const bmiP = bmiRate(input.bmi_range, data);

  const percentage = ageP * heightP * incomeP * maritalP * bmiP;
  const relevantPopulation = input.gender_target === 'male' ? data.male_population : data.female_population;

  return {
    percentage,
    matching_population: Math.round(relevantPopulation * percentage),
    total_population: relevantPopulation
  };
}
