import type { MLStatus } from "../../types/hives";

export function MLBadge({ status }: { status: MLStatus }) {
  if (status === "queued") {
    return (
      <span className="inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-600">
        Aguardando
      </span>
    );
  }

  if (status === "done") {
    return (
      <span className="inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
        Concluído
      </span>
    );
  }

  return (
    <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-700">
      <span className="w-2.5 h-2.5 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
      Processando
    </span>
  );
}
