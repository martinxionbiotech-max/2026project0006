export const countries = [
  { value: 'usa', label: 'United States', multiplier: 1 },
  { value: 'uk', label: 'United Kingdom', multiplier: 0.86 },
  { value: 'canada', label: 'Canada', multiplier: 0.91 },
  { value: 'australia', label: 'Australia', multiplier: 0.95 }
];

export function getCountryMultiplier(value) {
  return countries.find((c) => c.value === value)?.multiplier ?? 1;
}
