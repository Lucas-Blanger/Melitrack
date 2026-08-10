/* eslint-disable react-refresh/only-export-components */
import logo from "../assets/Melitrack.png";

export type HealthLevel = "excelente" | "boa" | "regular" | "ruim" | "crítica";
export type HiveType = "caixa" | "isca";
export type AnalysisStatus = "pending" | "processed" | "failed";

export const healthConfig: Record<
  HealthLevel,
  { label: string; bg: string; text: string; dot: string }
> = {
  excelente: {
    label: "Excelente",
    bg: "#dcfce7",
    text: "#15803d",
    dot: "#16a34a",
  },
  boa: { label: "Boa", bg: "#ccfbf1", text: "#0f766e", dot: "#0d9488" },
  regular: { label: "Regular", bg: "#fef3c7", text: "#b45309", dot: "#d97706" },
  ruim: { label: "Ruim", bg: "#ffedd5", text: "#c2410c", dot: "#ea580c" },
  crítica: { label: "Crítica", bg: "#fee2e2", text: "#b91c1c", dot: "#dc2626" },
};

export function MelitrackLogo({ size = 120 }: { size?: number }) {
  return <img src={logo} alt="Melitrack" width={size} height={size} />;
}

export function HealthBadge({ health }: { health: HealthLevel }) {
  const cfg = healthConfig[health];
  return (
    <span
      style={{ backgroundColor: cfg.bg, color: cfg.text }}
      className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium flex-shrink-0"
    >
      <span
        className="w-1.5 h-1.5 rounded-full flex-shrink-0"
        style={{ backgroundColor: cfg.dot }}
      />
      {cfg.label}
    </span>
  );
}

export function HealthDot({ health }: { health: HealthLevel }) {
  return (
    <span
      className="w-2.5 h-2.5 rounded-full flex-shrink-0 ring-2 ring-white"
      style={{ backgroundColor: healthConfig[health].dot }}
    />
  );
}

export function TypeBadge({ type }: { type: HiveType }) {
  const label = type === "caixa" ? "Caixa" : "Isca";

  return (
    <span
      className={`inline-flex px-2 py-0.5 rounded text-xs font-medium ${
        type === "caixa"
          ? "bg-blue-100 text-blue-700"
          : "bg-purple-100 text-purple-700"
      }`}
    >
      {label}
    </span>
  );
}

export function MLBadge({ status }: { status: AnalysisStatus }) {
  if (status === "pending")
    return (
      <span className="inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-600">
        Aguardando
      </span>
    );
  if (status === "processed")
    return (
      <span className="inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
        Concluído
      </span>
    );
  return (
    <span className="inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-700">
      Falhou
    </span>
  );
}

export function HoneycombPattern({ opacity = 0.07 }: { opacity?: number }) {
  return (
    <svg
      aria-hidden="true"
      style={{
        position: "absolute",
        inset: 0,
        width: "100%",
        height: "100%",
        opacity,
        pointerEvents: "none",
      }}
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <pattern
          id="honeycomb"
          x="0"
          y="0"
          width="56"
          height="97"
          patternUnits="userSpaceOnUse"
        >
          <polygon
            points="28,3 53,17 53,45 28,59 3,45 3,17"
            fill="none"
            stroke="#1D6A4A"
            strokeWidth="1.2"
          />
          <polygon
            points="0,50 25,64 25,92 0,106 -25,92 -25,64"
            fill="none"
            stroke="#1D6A4A"
            strokeWidth="1.2"
          />
          <polygon
            points="56,50 81,64 81,92 56,106 31,92 31,64"
            fill="none"
            stroke="#1D6A4A"
            strokeWidth="1.2"
          />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#honeycomb)" />
    </svg>
  );
}

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

export function Card({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`bg-white rounded-xl border ${className}`}
      style={{ borderColor: "#e8e4dc" }}
    >
      {children}
    </div>
  );
}
