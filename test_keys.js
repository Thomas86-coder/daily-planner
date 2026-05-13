function getISOWeekKey(dateStr) {
  const d = new Date(dateStr);
  d.setHours(0, 0, 0, 0);
  d.setDate(d.getDate() + 3 - (d.getDay() + 6) % 7);
  const week1 = new Date(d.getFullYear(), 0, 4);
  const weekNumber = 1 + Math.round(((d.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
  return `${d.getFullYear()}-${String(weekNumber).padStart(2, '0')}`;
}

console.log("Key for '2026-04-26':", getISOWeekKey('2026-04-26'));
console.log("Key for '2026-04-20':", getISOWeekKey('2026-04-20'));
