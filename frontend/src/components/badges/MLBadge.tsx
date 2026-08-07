import type { AnalysisStatus } from "../../types/hives";

export function MLBadge({ status }: { status: AnalysisStatus }) {
  if (status === "pending") {
    return (
      <span className="inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-600">
        Aguardando
      </span>
    );
  }

  if (status === "processed") {
    return (
      <span className="inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
        Concluído
      </span>
    );
  }

  return (
    <span className="inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-700">
      Falhou
    </span>
  );
}
