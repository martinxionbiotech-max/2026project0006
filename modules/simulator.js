import { calculateDatingPool } from './datingPool.js';

export function runRealityAdjustment(baseInput, data) {
  const scenarios = [185, 180, 175].map((height) => {
    const result = calculateDatingPool({ ...baseInput, height_min: height }, data);
    return {
      height,
      percentage: result.percentage,
      population: result.matching_population
    };
  });

  return scenarios;
}
