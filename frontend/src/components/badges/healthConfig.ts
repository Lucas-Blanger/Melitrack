import type { HealthLevel } from "../../types/hives";

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
