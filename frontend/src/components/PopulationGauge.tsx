export function PopulationGauge({
  percent,
  label,
}: {
  percent: number;
  label: string;
}) {
  const r = 58;
  const pathLength = Math.PI * r;
  const offset = pathLength * (1 - percent / 100);
  const color =
    percent > 75
      ? "#dc2626"
      : percent > 50
        ? "#E8A020"
        : percent > 25
          ? "#1D6A4A"
          : "#6b7280";

  return (
    <div className="flex flex-col items-center">
      <svg viewBox="0 0 140 82" width="180" height="106">
        <path
          d="M 12 75 A 58 58 0 0 1 128 75"
          fill="none"
          stroke="#f0ece4"
          strokeWidth="11"
          strokeLinecap="round"
        />
        <path
          d="M 12 75 A 58 58 0 0 1 128 75"
          fill="none"
          stroke={color}
          strokeWidth="11"
          strokeLinecap="round"
          strokeDasharray={pathLength}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 1s ease, stroke 0.5s ease" }}
        />
        <text
          x="70"
          y="68"
          textAnchor="middle"
          fontSize="20"
          fontWeight="700"
          fill="#1a1a1a"
          fontFamily="Inter, sans-serif"
        >
          {percent}%
        </text>
      </svg>
      <span
        className="text-xs font-semibold px-3 py-1 rounded-full -mt-2"
        style={{ backgroundColor: color + "20", color }}
      >
        {label}
      </span>
    </div>
  );
}
