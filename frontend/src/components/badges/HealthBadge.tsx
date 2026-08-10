import type { HealthLevel } from "../../types/hives";
import { healthConfig } from "./healthConfig";

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
