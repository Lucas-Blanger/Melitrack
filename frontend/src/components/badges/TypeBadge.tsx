import type { HiveType } from "../../types/hives";

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
