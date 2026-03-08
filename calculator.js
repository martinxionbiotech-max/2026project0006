import { calculateDatingPool } from './modules/datingPool.js';
import { calculateMarketValue } from './modules/marketValue.js';
import { calculateCompetitionRatio } from './modules/competition.js';
import { runRealityAdjustment } from './modules/simulator.js';
import { calculateFutureDatingProbability } from './modules/futureProbability.js';

export function buildRealityReport(inputs, countryData) {
  const datingPool = calculateDatingPool(inputs.poolInput, countryData);
  const marketValue = calculateMarketValue(inputs.marketInput);
  const competition = calculateCompetitionRatio(
    datingPool.percentage,
    countryData.female_population,
    countryData.male_population
  );
  const simulator = runRealityAdjustment(inputs.poolInput, countryData);
  const future = calculateFutureDatingProbability({
    age: inputs.marketInput.age,
    dating_pool_size: datingPool.matching_population,
    city_population: countryData.total_population,
    marriage_rate: countryData.marriage_rate
  });

  return { datingPool, marketValue, competition, simulator, future };
}

export function calculateDatingPoolApi(input, countryData) {
  const result = calculateDatingPool({
    gender_target: input.gender_target ?? 'male',
    age_min: input.age_min,
    age_max: input.age_max,
    height_min: input.height,
    income_min: input.income,
    marital_status: 'single',
    bmi_range: 'non_obese',
    country: input.country ?? 'usa'
  }, countryData);

  return {
    percentage: Number(result.percentage.toFixed(4)),
    population: result.matching_population
  };
}
