function getScoreLevel(score) {
  if (score >= 90) return "high";
  if (score >= 60) return "good";
  if (score >= 30) return "medium";
  return "low";
}

export default function ScoreGauge({ score }) {
  const percentage = Math.round(Math.min(100, Math.max(0, score * 100)));
  const level = getScoreLevel(percentage);

  return (
    <div
      className={`score-gauge score-gauge-${level}`}
      role="img"
      aria-label={`Điểm phù hợp ${percentage}%`}
      style={{ "--score-angle": `${percentage * 3.6}deg` }}
    >
      <div className="score-gauge-inner">
        <strong>{percentage}%</strong>
        <span>PHÙ HỢP</span>
      </div>
    </div>
  );
}
