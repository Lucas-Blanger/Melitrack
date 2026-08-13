import {
  AlertCircle,
  AlertTriangle,
  Boxes,
  Brain,
  Calendar,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  ClipboardCheck,
  Cpu,
  Droplets,
  FileText,
  MapPin,
  Pencil,
  Plus,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  Users,
} from "lucide-react";
import {
  useEffect,
  useState,
  type FormEvent,
  type ReactNode,
} from "react";
import { useParams } from "react-router-dom";
import {
  correctInspectionAnalysis,
  createHarvest,
  createInspection,
  getHive,
  listHivePhotos,
  getInspectionAnalysis,
  listHarvestsByHive,
  listInspectionsByHive,
  listProducts,
  uploadInspectionPhoto,
} from "../api/hives";
import { HealthBadge } from "../components/badges/HealthBadge";
import { MLBadge } from "../components/badges/MLBadge";
import { TypeBadge } from "../components/badges/TypeBadge";
import { Card } from "../components/Card";
import { PopulationGauge } from "../components/PopulationGauge";
import {
  Field,
  Select,
  TextArea,
  TextInput,
} from "../components/ui/FormControls";
import { Modal } from "../components/ui/Modal";
import { LoadingState, PageState } from "../components/ui/PageState";
import { useAsync } from "../hooks/useAsync";
import { formatDate, formatDateTime } from "../lib/format";
import type {
  Analysis,
  MLAnalysisResult,
  Harvest,
  HealthLevel,
  Hive,
  Inspection,
  Product,
} from "../types/hives";

type Tab = "inspections" | "harvests" | "ml";

interface DetailData {
  hive: Hive;
  inspections: Inspection[];
  harvests: Harvest[];
  products: Product[];
  analysis: Analysis | null;
}

export default function HiveDetail() {
  const { hiveId } = useParams();
  const [tab, setTab] = useState<Tab>("inspections");
  const [showInspectionModal, setShowInspectionModal] = useState(false);
  const [showHarvestModal, setShowHarvestModal] = useState(false);
  const { data, loading, error, reload } = useAsync(
    () => loadDetail(hiveId ?? ""),
    [hiveId],
  );
  const [photoUrl, setPhotoUrl] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    void (hiveId ? listHivePhotos(hiveId) : Promise.resolve([]))
      .then((photos) => {
        if (active) {
          setPhotoUrl(photos[0]?.data_url ?? null);
        }
      })
      .catch(() => {
        if (active) {
          setPhotoUrl(null);
        }
      });

    return () => {
      active = false;
    };
  }, [hiveId]);

  if (!hiveId) {
    return (
      <PageState title="Colmeia não encontrada" icon={<Boxes size={24} />} />
    );
  }

  if (loading) return <LoadingState />;
  if (error || !data) {
    return (
      <PageState
        title="Não foi possível carregar a colmeia"
        description={error ?? "Tente novamente em instantes."}
        icon={<Boxes size={24} />}
      />
    );
  }

  const latestInspection = data.inspections[0];
  const health = latestInspection?.health ?? "regular";

  return (
    <div className="mx-auto max-w-screen-xl p-5 sm:p-8">
      <div className="mb-7 grid gap-7 xl:grid-cols-5">
        <div className="xl:col-span-3">
          <div
            className="relative flex h-80 items-center justify-center overflow-hidden rounded-xl bg-[#d4eddf]"
            style={{
              backgroundImage: photoUrl ? `url(${photoUrl})` : undefined,
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}
          >
            {!photoUrl && <Boxes size={74} className="text-[#1D6A4A]" />}
            <div className="absolute inset-0 bg-gradient-to-t from-black/45 to-transparent" />
            <div className="absolute bottom-0 left-0 p-5">
              <h1 className="mb-1 text-2xl font-bold text-white">
                {data.hive.name}
              </h1>
              <div className="flex items-center gap-2">
                <HealthBadge health={health} />
                <TypeBadge type={data.hive.type} />
              </div>
            </div>
          </div>
        </div>

        <Card className="flex flex-col gap-4 p-6 xl:col-span-2">
          <h2 className="mb-1 text-sm font-semibold text-neutral-800">
            Informações
          </h2>
          <InfoRow label="Espécie" value={data.hive.species} />
          <InfoRow label="Tipo" value={<TypeBadge type={data.hive.type} />} />
          <InfoRow
            label="Saúde atual"
            value={<HealthBadge health={health} />}
          />
          <InfoRow
            label="Localização"
            value={
              <span className="flex items-center gap-1.5 text-sm text-neutral-700">
                <MapPin size={13} className="text-[#1D6A4A]" />
                {data.hive.location_description || "Não informada"}
              </span>
            }
          />
          <InfoRow
            label="Notas"
            value={data.hive.notes || "Nenhuma nota cadastrada"}
          />
        </Card>
      </div>

      <div className="mb-5 flex flex-wrap items-center justify-between gap-4">
        <div className="flex rounded-lg bg-[#ede9df] p-1">
          {[
            ["inspections", "Inspeções"],
            ["harvests", "Colheitas"],
            ["ml", "Análise IA"],
          ].map(([id, label]) => (
            <button
              key={id}
              type="button"
              onClick={() => setTab(id as Tab)}
              className={`rounded-md px-4 py-2 text-sm font-medium transition-colors ${
                tab === id
                  ? "bg-white text-[#1D6A4A] shadow-sm"
                  : "text-neutral-600"
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        {tab === "inspections" && (
          <button
            type="button"
            onClick={() => setShowInspectionModal(true)}
            className="inline-flex items-center gap-2 rounded-lg bg-[#1D6A4A] px-4 py-2.5 text-sm font-medium text-white"
          >
            <Plus size={15} />
            Nova Inspeção
          </button>
        )}
        {tab === "harvests" && (
          <button
            type="button"
            onClick={() => setShowHarvestModal(true)}
            className="inline-flex items-center gap-2 rounded-lg bg-[#1D6A4A] px-4 py-2.5 text-sm font-medium text-white"
          >
            <Plus size={15} />
            Nova Colheita
          </button>
        )}
      </div>

      {tab === "inspections" && (
        <InspectionTab inspections={data.inspections} />
      )}
      {tab === "harvests" && (
        <HarvestTab harvests={data.harvests} products={data.products} />
      )}
      {tab === "ml" && (
        <AnalysisTab
          analysis={data.analysis}
          latestInspection={latestInspection}
          onCorrected={() => void reload()}
        />
      )}

      {showInspectionModal && (
        <NewInspectionModal
          hiveId={data.hive.id}
          onClose={() => setShowInspectionModal(false)}
          onCreated={() => {
            setShowInspectionModal(false);
            void reload();
          }}
        />
      )}
      {showHarvestModal && (
        <NewHarvestModal
          hiveId={data.hive.id}
          products={data.products}
          onClose={() => setShowHarvestModal(false)}
          onCreated={() => {
            setShowHarvestModal(false);
            void reload();
          }}
        />
      )}
    </div>
  );
}

function InspectionTab({ inspections }: { inspections: Inspection[] }) {
  if (inspections.length === 0) {
    return (
      <PageState
        title="Nenhuma inspeção registrada"
        description="Crie uma inspeção para acompanhar saúde, rainha, mel e população."
        icon={<ClipboardCheck size={24} />}
      />
    );
  }

  return (
    <Card className="overflow-hidden">
      <table className="w-full text-sm">
        <thead className="border-b border-[#e8e4dc] bg-[#fafaf8] text-left text-xs text-neutral-500">
          <tr>
            <th className="px-4 py-3 font-medium">Data</th>
            <th className="px-4 py-3 font-medium">Saúde</th>
            <th className="px-4 py-3 font-medium">Rainha</th>
            <th className="px-4 py-3 font-medium">Mel</th>
            <th className="px-4 py-3 font-medium">População</th>
            <th className="px-4 py-3 font-medium">Notas</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-[#f0ece4]">
          {inspections.map((inspection) => (
            <tr key={inspection.id}>
              <td className="px-4 py-3 text-neutral-700">
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
              <td className="px-4 py-3 text-neutral-600">
                {inspection.population_estimate || "Não informada"}
              </td>
              <td className="max-w-xs px-4 py-3 text-neutral-500">
                {inspection.notes || "Sem notas"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  );
}

function HarvestTab({
  harvests,
  products,
}: {
  harvests: Harvest[];
  products: Product[];
}) {
  const productName = (id: number) =>
    products.find((product) => product.id === id)?.name ?? `Produto ${id}`;

  if (harvests.length === 0) {
    return (
      <PageState
        title="Nenhuma colheita registrada"
        description="Registre mel, própolis, cera ou outros produtos vinculados à colmeia."
        icon={<Droplets size={24} />}
      />
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {harvests.map((harvest) => (
        <Card key={harvest.id} className="p-5">
          <div className="mb-4 flex items-start justify-between">
            <div>
              <h3 className="text-sm font-semibold text-neutral-800">
                {productName(harvest.product_id)}
              </h3>
              <p className="mt-1 flex items-center gap-1 text-xs text-neutral-500">
                <Calendar size={12} />
                {formatDate(harvest.harvested_at)}
              </p>
            </div>
            <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-700">
              {harvest.quantity} {harvest.unit}
            </span>
          </div>
          <p className="text-sm leading-relaxed text-neutral-600">
            {harvest.quality_notes || "Sem notas de qualidade."}
          </p>
        </Card>
      ))}
    </div>
  );
}

function AnalysisTab({
  analysis,
  latestInspection,
  onCorrected,
}: {
  analysis: Analysis | null;
  latestInspection?: Inspection;
  onCorrected: () => void;
}) {
  const [showRawJson, setShowRawJson] = useState(false);
  const [showCorrectionModal, setShowCorrectionModal] = useState(false);

  if (!latestInspection) {
    return (
      <PageState
        title="Análise indisponível"
        description="Cadastre uma inspeção e envie fotos para iniciar a análise por IA."
        icon={<Brain size={24} />}
      />
    );
  }

  if (!analysis) {
    return (
      <PageState
        title="Análise aguardando imagens"
        description="O backend retornará uma análise em tempo real após o envio de fotos da inspeção."
        icon={<Brain size={24} />}
      />
    );
  }

  const result = analysis.result;
  const anomaly = result?.anomaly;
  const population = result?.population;

  const scoreLabels: Record<string, string> = {
    fungi: "Fungos / Mofo",
    empty_cells: "Células Vazias",
    disease_signs: "Sinais de Doenças",
  };

  const confidencePct =
    analysis.confidence !== null ? Math.round(analysis.confidence * 100) : null;

  return (
    <div className="space-y-6">
      {/* Cards de Resumo no Topo */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {/* Card 1: Status & Modelo */}
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-[#1D6A4A]">
              <Cpu size={20} />
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-medium text-neutral-400">Modelo IA</p>
              <p className="truncate text-sm font-bold text-neutral-800">
                {analysis.model_name || "EfficientNetB0"}
              </p>
            </div>
            <MLBadge status={analysis.status} />
          </div>
          <div className="mt-3 border-t border-neutral-100 pt-2 text-xs text-neutral-400">
            Processado em: {formatDateTime(analysis.processed_at)}
          </div>
        </Card>

        {/* Card 2: Confiança do Modelo */}
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-amber-50 text-amber-600">
              <Sparkles size={20} />
            </div>
            <div>
              <p className="text-xs font-medium text-neutral-400">Confiança Geral</p>
              <p className="text-lg font-bold text-neutral-800">
                {confidencePct !== null ? `${confidencePct}%` : "—"}
              </p>
            </div>
          </div>
          {confidencePct !== null && (
            <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-neutral-100">
              <div
                className="h-full rounded-full bg-amber-500 transition-all duration-500"
                style={{ width: `${confidencePct}%` }}
              />
            </div>
          )}
        </Card>

        {/* Card 3: Saúde da Colmeia */}
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div
              className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${
                anomaly?.has_anomaly
                  ? "bg-rose-50 text-rose-600"
                  : "bg-emerald-50 text-emerald-600"
              }`}
            >
              {anomaly?.has_anomaly ? (
                <ShieldAlert size={20} />
              ) : (
                <ShieldCheck size={20} />
              )}
            </div>
            <div>
              <p className="text-xs font-medium text-neutral-400">Diagnóstico</p>
              <p
                className={`text-sm font-bold ${
                  anomaly?.has_anomaly ? "text-rose-600" : "text-emerald-700"
                }`}
              >
                {anomaly?.has_anomaly ? "Anomalia Detectada" : "Saudável / Sem Alertas"}
              </p>
            </div>
          </div>
          <div className="mt-3 border-t border-neutral-100 pt-2 text-xs text-neutral-400">
            {anomaly?.alerts?.length
              ? `${anomaly.alerts.length} alerta(s) identificado(s)`
              : "Nenhum sinal crítico"}
          </div>
        </Card>

        {/* Card 4: Nível Populacional */}
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
              <Users size={20} />
            </div>
            <div>
              <p className="text-xs font-medium text-neutral-400">População Estimada</p>
              <p className="text-sm font-bold capitalize text-neutral-800">
                {population?.level
                  ? `Nível ${population.level}`
                  : "Não estimada"}
              </p>
            </div>
          </div>
          <div className="mt-3 border-t border-neutral-100 pt-2 text-xs text-neutral-500">
            Est.: {population?.estimated_count || "—"} abelhas
          </div>
        </Card>
      </div>

      <Card className="p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <div className="flex items-center gap-2">
              <Pencil size={16} className="text-[#1D6A4A]" />
              <h2 className="text-sm font-semibold text-neutral-800">
                Correção humana
              </h2>
            </div>
            <p className="mt-1 text-sm text-neutral-500">
              Ajuste o diagnóstico da IA quando a inspeção em campo indicar outro resultado.
            </p>
            {analysis.corrected_at && (
              <p className="mt-2 text-xs font-medium text-[#1D6A4A]">
                Última correção: {formatDateTime(analysis.corrected_at)}
              </p>
            )}
          </div>
          <button
            type="button"
            onClick={() => setShowCorrectionModal(true)}
            className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#1D6A4A] px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-[#155438]"
          >
            <Pencil size={15} />
            {analysis.corrected_result ? "Editar Correção" : "Corrigir Resultado"}
          </button>
        </div>

        {analysis.corrected_result && (
          <div className="mt-5 grid gap-4 border-t border-neutral-100 pt-5 sm:grid-cols-2 xl:grid-cols-4">
            <CorrectionSummary
              label="Diagnóstico corrigido"
              value={
                analysis.corrected_result.anomaly?.has_anomaly
                  ? "Anomalia detectada"
                  : "Sem anomalia"
              }
            />
            <CorrectionSummary
              label="População corrigida"
              value={
                analysis.corrected_result.population?.level
                  ? `Nível ${analysis.corrected_result.population.level}`
                  : "Não informada"
              }
            />
            <CorrectionSummary
              label="Estimativa corrigida"
              value={analysis.corrected_result.population?.estimated_count || "Não informada"}
            />
            <CorrectionSummary
              label="Notas"
              value={analysis.correction_notes || "Sem notas"}
            />
          </div>
        )}
      </Card>

      {/* Caso haja mensagem de erro */}
      {analysis.error_message && (
        <div className="flex items-center gap-3 rounded-xl border border-rose-200 bg-rose-50/70 p-4 text-rose-700">
          <AlertCircle size={20} className="shrink-0" />
          <p className="text-sm font-medium">{analysis.error_message}</p>
        </div>
      )}

      {/* Grid Principal de Detalhes */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Painel de Anomalias & Saúde */}
        <Card className="p-6">
          <div className="mb-5 flex items-center justify-between border-b border-neutral-100 pb-3">
            <div className="flex items-center gap-2">
              <ShieldAlert size={18} className="text-neutral-500" />
              <h2 className="font-semibold text-neutral-800">
                Detecção de Anomalias
              </h2>
            </div>
            {anomaly?.has_anomaly ? (
              <span className="inline-flex items-center gap-1 rounded-full bg-rose-100 px-2.5 py-0.5 text-xs font-semibold text-rose-700">
                <AlertTriangle size={12} /> Alerta Ativo
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 rounded-full bg-emerald-100 px-2.5 py-0.5 text-xs font-semibold text-emerald-700">
                <CheckCircle2 size={12} /> OK
              </span>
            )}
          </div>

          {/* Alertas Ativos */}
          {anomaly?.alerts && anomaly.alerts.length > 0 && (
            <div className="mb-5 space-y-2.5">
              <p className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
                Alertas identificados pela IA
              </p>
              {anomaly.alerts.map((alert, idx) => (
                <div
                  key={idx}
                  className="flex items-start justify-between rounded-xl border border-rose-100 bg-rose-50/60 p-3 text-xs"
                >
                  <div className="flex gap-2.5">
                    <AlertTriangle size={16} className="mt-0.5 shrink-0 text-rose-500" />
                    <div>
                      <p className="font-semibold text-rose-900">{alert.description}</p>
                      <p className="mt-0.5 text-rose-600">Categoria: {alert.label}</p>
                    </div>
                  </div>
                  <span className="rounded-md bg-rose-200/60 px-2 py-0.5 font-bold text-rose-800">
                    {Math.round(alert.score * 100)}%
                  </span>
                </div>
              ))}
            </div>
          )}

          {/* Barras de Probabilidade de Riscos */}
          <div className="space-y-4">
            <p className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
              Probabilidade por Indicador
            </p>
            {anomaly?.scores &&
              Object.entries(anomaly.scores).map(([key, rawScore]) => {
                const score = typeof rawScore === "number" ? rawScore : 0;
                const percent = Math.round(score * 100);
                const label = scoreLabels[key] || key;
                const isHigh = percent >= 50;

                return (
                  <div key={key} className="space-y-1.5">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-medium text-neutral-700">{label}</span>
                      <span
                        className={`font-semibold ${
                          isHigh ? "text-rose-600" : "text-neutral-500"
                        }`}
                      >
                        {percent}%
                      </span>
                    </div>
                    <div className="h-2 w-full overflow-hidden rounded-full bg-neutral-100">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${
                          isHigh ? "bg-rose-500" : "bg-emerald-500"
                        }`}
                        style={{ width: `${percent}%` }}
                      />
                    </div>
                  </div>
                );
              })}
          </div>
        </Card>

        {/* Painel de População */}
        <Card className="p-6">
          <div className="mb-5 flex items-center justify-between border-b border-neutral-100 pb-3">
            <div className="flex items-center gap-2">
              <Users size={18} className="text-neutral-500" />
              <h2 className="font-semibold text-neutral-800">
                Densidade Populacional
              </h2>
            </div>
            {population?.level && (
              <span className="rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-semibold text-blue-700 capitalize">
                Nível {population.level}
              </span>
            )}
          </div>

          <div className="flex flex-col items-center justify-center py-4">
            <PopulationGauge
              percent={
                typeof population?.density_score === "number"
                  ? Math.round(population.density_score * 100)
                  : latestInspection?.honey_level ?? 50
              }
              label={
                population?.level
                  ? `Nível ${population.level}`
                  : populationLabel(latestInspection?.honey_level ?? 50)
              }
            />

            {population?.estimated_count && (
              <div className="mt-6 flex items-center gap-3 rounded-xl border border-neutral-100 bg-[#fafaf8] px-5 py-3 text-center">
                <Users size={20} className="text-[#1D6A4A]" />
                <div className="text-left">
                  <p className="text-xs text-neutral-400">Estimativa de indivíduos</p>
                  <p className="text-sm font-bold text-neutral-800">
                    {population.estimated_count} abelhas
                  </p>
                </div>
              </div>
            )}
          </div>
        </Card>
      </div>

      {/* JSON Bruto Colapsável */}
      <Card className="overflow-hidden">
        <button
          type="button"
          onClick={() => setShowRawJson(!showRawJson)}
          className="flex w-full items-center justify-between p-4 text-xs font-semibold text-neutral-500 hover:bg-neutral-50"
        >
          <div className="flex items-center gap-2">
            <FileText size={15} />
            <span>Dados Técnicos Brutos (JSON)</span>
          </div>
          {showRawJson ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>

        {showRawJson && (
          <div className="border-t border-neutral-100 bg-[#fafaf8] p-4">
            <pre className="max-h-64 overflow-auto text-xs text-neutral-600">
              {JSON.stringify(analysis.result ?? {}, null, 2)}
            </pre>
          </div>
        )}
      </Card>

      {showCorrectionModal && (
        <AnalysisCorrectionModal
          inspectionId={latestInspection.id}
          analysis={analysis}
          onClose={() => setShowCorrectionModal(false)}
          onSaved={() => {
            setShowCorrectionModal(false);
            onCorrected();
          }}
        />
      )}
    </div>
  );
}

function CorrectionSummary({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-[#fafaf8] p-3">
      <p className="text-xs font-medium text-neutral-400">{label}</p>
      <p className="mt-1 text-sm font-semibold text-neutral-800">{value}</p>
    </div>
  );
}

function AnalysisCorrectionModal({
  inspectionId,
  analysis,
  onClose,
  onSaved,
}: {
  inspectionId: string;
  analysis: Analysis;
  onClose: () => void;
  onSaved: () => void;
}) {
  const source = analysis.corrected_result ?? analysis.result ?? {};
  const sourceAnomaly = source.anomaly;
  const sourcePopulation = source.population;
  const sourceScores = sourceAnomaly?.scores ?? {};
  const [hasAnomaly, setHasAnomaly] = useState(
    sourceAnomaly?.has_anomaly ? "true" : "false",
  );
  const [populationLevel, setPopulationLevel] = useState(
    sourcePopulation?.level ?? "",
  );
  const [estimatedCount, setEstimatedCount] = useState(
    sourcePopulation?.estimated_count ?? "",
  );
  const [densityScore, setDensityScore] = useState(
    String(toPercent(sourcePopulation?.density_score)),
  );
  const [fungiScore, setFungiScore] = useState(String(toPercent(sourceScores.fungi)));
  const [emptyCellsScore, setEmptyCellsScore] = useState(
    String(toPercent(sourceScores.empty_cells)),
  );
  const [diseaseScore, setDiseaseScore] = useState(
    String(toPercent(sourceScores.disease_signs)),
  );
  const [notes, setNotes] = useState(analysis.correction_notes ?? "");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setSubmitting(true);

    const correctedResult: MLAnalysisResult = {
      ...analysis.result,
      anomaly: {
        ...analysis.result?.anomaly,
        has_anomaly: hasAnomaly === "true",
        alerts: hasAnomaly === "true" ? analysis.result?.anomaly?.alerts ?? [] : [],
        scores: {
          ...analysis.result?.anomaly?.scores,
          fungi: fromPercent(fungiScore),
          empty_cells: fromPercent(emptyCellsScore),
          disease_signs: fromPercent(diseaseScore),
        },
      },
      population: {
        ...analysis.result?.population,
        level: populationLevel || undefined,
        density_score: fromPercent(densityScore),
        estimated_count: estimatedCount || undefined,
      },
      population_percent: Number(densityScore || 0),
    };

    try {
      await correctInspectionAnalysis(inspectionId, {
        corrected_result: correctedResult,
        correction_notes: notes || null,
      });
      onSaved();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Não foi possível salvar.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Modal title="Corrigir Resultado da IA" onClose={onClose}>
      <form onSubmit={submit} className="space-y-4">
        <Field label="Diagnóstico real">
          <Select value={hasAnomaly} onChange={setHasAnomaly} className="w-full">
            <option value="false">Sem anomalia</option>
            <option value="true">Anomalia detectada</option>
          </Select>
        </Field>

        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Nível populacional">
            <Select
              value={populationLevel}
              onChange={setPopulationLevel}
              className="w-full"
            >
              <option value="">Não informar</option>
              <option value="baixo">Baixo</option>
              <option value="médio">Médio</option>
              <option value="alto">Alto</option>
            </Select>
          </Field>
          <Field label="Estimativa de indivíduos">
            <TextInput
              value={estimatedCount}
              onChange={(event) => setEstimatedCount(event.target.value)}
              placeholder="Ex.: 3.000"
            />
          </Field>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Densidade (%)">
            <TextInput
              type="number"
              min={0}
              max={100}
              value={densityScore}
              onChange={(event) => setDensityScore(event.target.value)}
            />
          </Field>
          <Field label="Fungos / Mofo (%)">
            <TextInput
              type="number"
              min={0}
              max={100}
              value={fungiScore}
              onChange={(event) => setFungiScore(event.target.value)}
            />
          </Field>
          <Field label="Células vazias (%)">
            <TextInput
              type="number"
              min={0}
              max={100}
              value={emptyCellsScore}
              onChange={(event) => setEmptyCellsScore(event.target.value)}
            />
          </Field>
          <Field label="Sinais de doenças (%)">
            <TextInput
              type="number"
              min={0}
              max={100}
              value={diseaseScore}
              onChange={(event) => setDiseaseScore(event.target.value)}
            />
          </Field>
        </div>

        <Field label="Notas da correção">
          <TextArea
            value={notes}
            onChange={(event) => setNotes(event.target.value)}
            placeholder="Explique o que foi observado na revisão em campo."
          />
        </Field>

        {error && <p className="text-sm text-red-600">{error}</p>}
        <ModalActions onClose={onClose} submitting={submitting} />
      </form>
    </Modal>
  );
}

function toPercent(value: number | undefined) {
  if (typeof value !== "number") return 0;
  return Math.round(value * 100);
}

function fromPercent(value: string) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return 0;
  return Math.max(0, Math.min(100, numeric)) / 100;
}

function NewInspectionModal({
  hiveId,
  onClose,
  onCreated,
}: {
  hiveId: string;
  onClose: () => void;
  onCreated: () => void;
}) {
  const [health, setHealth] = useState<HealthLevel>("boa");
  const [queenSeen, setQueenSeen] = useState("true");
  const [honeyLevel, setHoneyLevel] = useState("50");
  const [population, setPopulation] = useState("");
  const [notes, setNotes] = useState("");
  const [photoFile, setPhotoFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      const inspection = await createInspection({
        hive_id: hiveId,
        health,
        queen_seen: queenSeen === "true",
        honey_level: Number(honeyLevel),
        population_estimate: population || null,
        notes: notes || null,
      });

      if (photoFile) {
        await uploadInspectionPhoto(inspection.id, photoFile);
      }

      onCreated();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Não foi possível salvar.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Modal title="Nova Inspeção" onClose={onClose}>
      <form onSubmit={submit} className="space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Saúde">
            <Select
              value={health}
              onChange={(value) => setHealth(value as HealthLevel)}
              className="w-full"
            >
              <option value="excelente">Excelente</option>
              <option value="boa">Boa</option>
              <option value="regular">Regular</option>
              <option value="ruim">Ruim</option>
              <option value="crítica">Crítica</option>
            </Select>
          </Field>
          <Field label="Rainha">
            <Select
              value={queenSeen}
              onChange={setQueenSeen}
              className="w-full"
            >
              <option value="true">Vista</option>
              <option value="false">Não vista</option>
            </Select>
          </Field>
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Mel (%)">
            <TextInput
              type="number"
              min={0}
              max={100}
              value={honeyLevel}
              onChange={(event) => setHoneyLevel(event.target.value)}
            />
          </Field>
          <Field label="População estimada">
            <TextInput
              value={population}
              onChange={(event) => setPopulation(event.target.value)}
              placeholder="Ex.: 3.000 abelhas"
            />
          </Field>
        </div>
        <Field label="Notas">
          <TextArea
            value={notes}
            onChange={(event) => setNotes(event.target.value)}
          />
        </Field>
        <Field label="Foto da inspeção">
          <input
            type="file"
            accept="image/*"
            onChange={(event) => setPhotoFile(event.target.files?.[0] ?? null)}
            className="w-full rounded-lg border border-[#ddd] bg-[#fafaf9] px-3 py-2 text-sm text-neutral-700"
          />
        </Field>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <ModalActions onClose={onClose} submitting={submitting} />
      </form>
    </Modal>
  );
}

function NewHarvestModal({
  hiveId,
  products,
  onClose,
  onCreated,
}: {
  hiveId: string;
  products: Product[];
  onClose: () => void;
  onCreated: () => void;
}) {
  const [productId, setProductId] = useState(String(products[0]?.id ?? ""));
  const [quantity, setQuantity] = useState("");
  const [unit, setUnit] = useState(products[0]?.unit ?? "");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      if (!productId) throw new Error("Cadastre um produto antes da colheita.");
      await createHarvest({
        hive_id: hiveId,
        product_id: Number(productId),
        quantity: Number(quantity),
        unit: unit || null,
        quality_notes: notes || null,
      });
      onCreated();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Não foi possível salvar.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Modal title="Nova Colheita" onClose={onClose}>
      <form onSubmit={submit} className="space-y-4">
        <Field label="Produto">
          <Select
            value={productId}
            onChange={(value) => {
              setProductId(value);
              setUnit(
                products.find((product) => String(product.id) === value)
                  ?.unit ?? "",
              );
            }}
            className="w-full"
          >
            {products.map((product) => (
              <option key={product.id} value={product.id}>
                {product.name}
              </option>
            ))}
          </Select>
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Quantidade">
            <TextInput
              type="number"
              min={0}
              step="0.01"
              value={quantity}
              onChange={(event) => setQuantity(event.target.value)}
              required
            />
          </Field>
          <Field label="Unidade">
            <TextInput
              value={unit}
              onChange={(event) => setUnit(event.target.value)}
            />
          </Field>
        </div>
        <Field label="Notas de qualidade">
          <TextArea
            value={notes}
            onChange={(event) => setNotes(event.target.value)}
          />
        </Field>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <ModalActions onClose={onClose} submitting={submitting} />
      </form>
    </Modal>
  );
}

function ModalActions({
  onClose,
  submitting,
}: {
  onClose: () => void;
  submitting: boolean;
}) {
  return (
    <div className="flex justify-end gap-2 pt-2">
      <button
        type="button"
        onClick={onClose}
        className="rounded-lg px-4 py-2 text-sm font-medium text-neutral-600 hover:bg-neutral-100"
      >
        Cancelar
      </button>
      <button
        type="submit"
        disabled={submitting}
        className="rounded-lg bg-[#1D6A4A] px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
      >
        {submitting ? "Salvando..." : "Salvar"}
      </button>
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: ReactNode }) {
  return (
    <div>
      <p className="mb-1 text-xs font-medium uppercase tracking-wide text-neutral-400">
        {label}
      </p>
      <div className="text-sm leading-relaxed text-neutral-700">{value}</div>
    </div>
  );
}

function populationLabel(percent: number) {
  if (percent >= 75) return "Alta";
  if (percent >= 50) return "Média";
  if (percent >= 25) return "Baixa";
  return "Muito baixa";
}

async function loadDetail(hiveId: string): Promise<DetailData> {
  const hive = await getHive(hiveId);
  const [inspections, harvests, products] = await Promise.all([
    listInspectionsByHive(hiveId),
    listHarvestsByHive(hiveId),
    listProducts(),
  ]);

  const analysis = inspections[0]
    ? await getInspectionAnalysis(inspections[0].id).catch(() => null)
    : null;

  return { hive, inspections, harvests, products, analysis };
}
