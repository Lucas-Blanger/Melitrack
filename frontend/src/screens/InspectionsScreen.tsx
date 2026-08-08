import { ClipboardCheck, Plus } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { listHives, listInspectionsByHive } from "../api/hives";
import { HealthBadge } from "../components/badges/HealthBadge";
import { Card } from "../components/Card";
import { LoadingState, PageState } from "../components/ui/PageState";
import { useAsync } from "../hooks/useAsync";
import { formatDate } from "../lib/format";
import type { Hive, Inspection } from "../types/hives";

interface Row {
  hive: Hive;
  inspection: Inspection;
}

export default function InspectionsScreen() {
  const navigate = useNavigate();
  const { data, loading, error } = useAsync(loadInspections, []);

  if (loading) return <LoadingState />;
  if (error) {
    return (
      <PageState
        title="Não foi possível carregar as inspeções"
        description={error}
        icon={<ClipboardCheck size={24} />}
      />
    );
  }

  const rows = data ?? [];

  return (
    <div className="mx-auto max-w-screen-xl p-5 sm:p-8">
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-neutral-800">Inspeções</h1>
          <p className="mt-1 text-sm text-neutral-500">
            Histórico completo de inspeções realizadas
          </p>
        </div>
        <button
          type="button"
          onClick={() => navigate("/hives")}
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#1D6A4A] px-4 py-2.5 text-sm font-medium text-white"
        >
          <Plus size={15} />
          Nova Inspeção
        </button>
      </div>

      {rows.length === 0 ? (
        <PageState
          title="Nenhuma inspeção registrada"
          description="Abra uma colmeia para criar a primeira inspeção."
          icon={<ClipboardCheck size={24} />}
        />
      ) : (
        <Card className="overflow-hidden">
          <table className="w-full text-sm">
            <thead className="border-b border-[#e8e4dc] bg-[#fafaf8] text-left text-xs text-neutral-500">
              <tr>
                <th className="px-4 py-3 font-medium">Colmeia</th>
                <th className="px-4 py-3 font-medium">Data</th>
                <th className="px-4 py-3 font-medium">Saúde</th>
                <th className="px-4 py-3 font-medium">Rainha</th>
                <th className="px-4 py-3 font-medium">Mel</th>
                <th className="px-4 py-3 font-medium">Notas</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#f0ece4]">
              {rows.map(({ hive, inspection }) => (
                <tr
                  key={inspection.id}
                  className="cursor-pointer transition-colors hover:bg-[#fafaf8]"
                  onClick={() => navigate(`/hives/${hive.id}`)}
                >
                  <td className="px-4 py-3 font-medium text-neutral-800">
                    {hive.name}
                  </td>
                  <td className="px-4 py-3 text-neutral-600">
                    {formatDate(inspection.inspected_at)}
                  </td>
                  <td className="px-4 py-3">
                    <HealthBadge health={inspection.health} />
                  </td>
                  <td className="px-4 py-3 text-neutral-600">
                    {inspection.queen_seen ? "Vista" : "Não vista"}
                  </td>
                  <td className="px-4 py-3 text-neutral-600">
                    {inspection.honey_level ?? 0}%
                  </td>
                  <td className="max-w-sm px-4 py-3 text-neutral-500">
                    {inspection.notes || "Sem notas"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      )}
    </div>
  );
}

async function loadInspections(): Promise<Row[]> {
  const hives = await listHives();
  const groups = await Promise.all(
    hives.map(async (hive) => ({
      hive,
      inspections: await listInspectionsByHive(hive.id).catch(() => []),
    })),
  );

  return groups
    .flatMap(({ hive, inspections }) =>
      inspections.map((inspection) => ({ hive, inspection })),
    )
    .sort(
      (a, b) =>
        new Date(b.inspection.inspected_at).getTime() -
        new Date(a.inspection.inspected_at).getTime(),
    );
}
