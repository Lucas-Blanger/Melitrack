import type { HealthLevel } from "../../types/hives";
import { healthConfig } from "./healthConfig";

export function HealthDot({ health }: { health: HealthLevel }) {
  return (
    <span
      className="w-2.5 h-2.5 rounded-full flex-shrink-0 ring-2 ring-white"
      style={{ backgroundColor: healthConfig[health].dot }}
    />
  );
}
