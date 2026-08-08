import {
  AlertTriangle,
  ArrowRight,
  Boxes,
  ClipboardCheck,
  Droplets,
  TrendingUp,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import {
  getDashboardOverview,
  getHarvestSummary,
  listHives,
  listInspectionsByHive,
} from "../api/hives";
import { HealthBadge } from "../components/badges/HealthBadge";
import { Card } from "../components/Card";
import { LoadingState, PageState } from "../components/ui/PageState";
import { useAsync } from "../hooks/useAsync";
import { daysSince, formatDate } from "../lib/format";
import type { Hive, Inspection } from "../types/hives";

interface DashboardData {
  totalHives: number;
  healthAlerts: number;
  lastInspection: Inspection | null;
  attention: Array<{ hive: Hive; inspection: Inspection }>;
  recent: Array<{ hive: Hive; inspection: Inspection }>;
  harvestTotal: number;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const { data, loading, error } = useAsync(loadDashboard, []);

  if (loading) return <LoadingState />;
  if (error || !data) {
    return (
      <PageState
        title="Não foi possível carregar o dashboard"
        description={error ?? "Tente novamente em instantes."}
        icon={<Boxes size={24} />}
      />
    );
  }

  const cards = [
    {
      label: "Total de Colmeias",
      value: String(data.totalHives),
      sub: "Registros ativos",
      icon: Boxes,
      iconColor: "#1D6A4A",
      iconBg: "#f0f8f4",
    },
    {
      label: "Última Inspeção",
      value: data.lastInspection ? (daysSince(data.lastInspection.inspected_at) ?? "recente") : "Sem dados",
      sub: data.lastInspection ? formatDate(data.lastInspection.inspected_at) : "Nenhuma inspeção cadastrada",
      icon: ClipboardCheck,
      iconColor: "#0d9488",
      iconBg: "#ccfbf1",
    },
    {
      label: "Colheita Total",
      value: data.harvestTotal.toLocaleString("pt-BR"),
      sub: "Quantidade somada no período",
      icon: Droplets,
      iconColor: "#E8A020",
      iconBg: "#fdf8ee",
    },
    {
      label: "Alertas Ativos",
      value: String(data.healthAlerts),
      sub: "Inspeções ruins ou críticas",
      icon: AlertTriangle,
      iconColor: "#dc2626",
      iconBg: "#fee2e2",
    },
  ];

  return (
    <div className="mx-auto max-w-screen-xl p-5 sm:p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-neutral-800">Dashboard</h1>
        <p className="mt-1 text-sm text-neutral-500">
          Visão geral operacional do meliponário
        </p>
      </div>

      <div className="mb-7 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {cards.map((card) => (
          <Card key={card.label} className="p-5">
            <div className="mb-4 flex items-center justify-between">
              <div
                className="flex h-9 w-9 items-center justify-center rounded-lg"
                style={{ backgroundColor: card.iconBg }}
              >
                <card.icon size={18} style={{ color: card.iconColor }} />
              </div>
              <TrendingUp size={13} className="text-emerald-600" />
            </div>
            <p className="mb-1 text-2xl font-bold leading-none text-neutral-800">
              {card.value}
            </p>
            <p className="mb-1.5 text-xs text-neutral-500">{card.label}</p>
            <p className="text-xs font-medium" style={{ color: card.iconColor }}>
              {card.sub}
            </p>
          </Card>
        ))}
      </div>

      <div className="mb-5 grid gap-5 xl:grid-cols-5">
        <Card className="p-5 xl:col-span-2">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-neutral-800">
              Precisam de atenção
            </h2>
            <span className="rounded-full bg-red-50 px-2 py-0.5 text-xs font-medium text-red-600">
              {data.attention.length} alertas
            </span>
          </div>

          {data.attention.length === 0 ? (
            <p className="rounded-lg bg-[#fafaf8] p-4 text-sm text-neutral-500">
              Nenhuma colmeia com última inspeção ruim ou crítica.
            </p>
          ) : (
            <div className="space-y-2.5">
              {data.attention.map(({ hive, inspection }) => (
                <button
                  key={inspection.id}
                  type="button"
                  onClick={() => navigate(`/hives/${hive.id}`)}
                  className="w-full rounded-xl border border-[#f0ece4] bg-[#fafaf8] p-3.5 text-left transition-colors hover:border-[#e0dbd2] hover:bg-[#f5f2ed]"
                >
                  <div className="mb-1.5 flex items-center justify-between gap-3">
                    <span className="text-sm font-medium text-neutral-800">
                      {hive.name}
                    </span>
                    <HealthBadge health={inspection.health} />
                  </div>
                  <p className="mb-2 text-xs text-neutral-500">
                    {hive.species} · {daysSince(inspection.inspected_at) ?? "sem data"}
                  </p>
                  <p className="flex items-center gap-1.5 text-xs text-neutral-600">
                    <AlertTriangle size={11} className="text-orange-600" />
                    Mel em {inspection.honey_level ?? 0}% e saúde {inspection.health}
                  </p>
                </button>
              ))}
            </div>
          )}

          <button
            type="button"
            onClick={() => navigate("/hives")}
            className="mt-4 flex w-full items-center justify-center gap-1.5 py-2 text-xs font-medium text-neutral-500 transition-colors hover:text-neutral-800"
          >
            Ver todas as colmeias
            <ArrowRight size={12} />
          </button>
        </Card>

        <Card className="p-5 xl:col-span-3">
          <div className="mb-5 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-neutral-800">
              Inspeções recentes
            </h2>
            <button
              type="button"
              onClick={() => navigate("/inspections")}
              className="flex items-center gap-1 text-xs text-neutral-500 transition-colors hover:text-neutral-800"
            >
              Ver todas
              <ArrowRight size={11} />
            </button>
          </div>

          {data.recent.length === 0 ? (
            <p className="rounded-lg bg-[#fafaf8] p-4 text-sm text-neutral-500">
              Ainda não há inspeções cadastradas.
            </p>
          ) : (
            <div>
              {data.recent.slice(0, 5).map(({ hive, inspection }, index) => (
                <div key={inspection.id} className="flex gap-4">
                  <div className="flex w-4 shrink-0 flex-col items-center">
                    <div className="mt-1 h-2 w-2 shrink-0 rounded-full bg-[#1D6A4A]" />
                    {index < data.recent.length - 1 && (
                      <div className="mt-1 min-h-8 flex-1 bg-[#e8e4dc] [width:1px]" />
                    )}
                  </div>
                  <div className="flex-1 pb-5">
                    <div className="mb-1 flex items-center justify-between gap-3">
                      <span className="text-sm font-medium text-neutral-800">
                        {hive.name}
                      </span>
                      <HealthBadge health={inspection.health} />
                    </div>
                    <div className="mb-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-neutral-500">
                      <span>{formatDate(inspection.inspected_at)}</span>
                      <span>
                        Rainha: {inspection.queen_seen ? "vista" : "não vista"}
                      </span>
                      <span>Mel: {inspection.honey_level ?? 0}%</span>
                    </div>
                    <HoneyBar value={inspection.honey_level ?? 0} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

function HoneyBar({ value }: { value: number }) {
  const color = value > 60 ? "#1D6A4A" : value > 30 ? "#E8A020" : "#dc2626";

  return (
    <div className="flex items-center gap-2">
      <div className="h-1 w-full max-w-40 rounded-full bg-[#f0ece4]">
        <div
          className="h-full rounded-full"
          style={{ width: `${value}%`, backgroundColor: color }}
        />
      </div>
      <span className="text-xs text-neutral-400">{value}% mel</span>
    </div>
  );
}

async function loadDashboard(): Promise<DashboardData> {
  const [overview, hives, harvestSummary] = await Promise.all([
    getDashboardOverview(),
    listHives(),
    getHarvestSummary(),
  ]);

  const inspectionsByHive = await Promise.all(
    hives.map(async (hive) => ({
      hive,
      inspections: await listInspectionsByHive(hive.id).catch(() => []),
    })),
  );

  const latestByHive = inspectionsByHive
    .map(({ hive, inspections }) => ({ hive, inspection: inspections[0] }))
    .filter((item): item is { hive: Hive; inspection: Inspection } => Boolean(item.inspection));

  const recent = latestByHive
    .flatMap(({ hive, inspection }) => [{ hive, inspection }])
    .sort(
      (a, b) =>
        new Date(b.inspection.inspected_at).getTime() -
        new Date(a.inspection.inspected_at).getTime(),
    );

  const attention = latestByHive.filter(({ inspection }) =>
    ["ruim", "crítica"].includes(inspection.health),
  );

  return {
    totalHives: overview.total_hives,
    healthAlerts: overview.health_alerts,
    lastInspection: overview.last_inspection,
    attention,
    recent,
    harvestTotal: harvestSummary.items.reduce(
      (sum, item) => sum + item.total_quantity,
      0,
    ),
  };
}
