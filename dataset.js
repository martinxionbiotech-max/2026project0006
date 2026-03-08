export const fallbackPopulationData = {
  usa: {
    total_population: 330000000,
    male_population: 165000000,
    female_population: 165000000,
    age_distribution: {
      '18-24': 0.12,
      '25-35': 0.18,
      '36-45': 0.16
    },
    height_over_175: 0.48,
    height_over_180: 0.15,
    height_over_185: 0.04,
    income_over_50000: 0.36,
    income_over_100000: 0.1,
    income_over_150000: 0.04,
    single_rate: 0.4,
    non_obese: 0.6,
    marriage_rate: 0.48
  }
};

export async function getPopulationData() {
  const response = await fetch('./api/populationData.json');
  if (!response.ok) return fallbackPopulationData;
  return response.json();
}
