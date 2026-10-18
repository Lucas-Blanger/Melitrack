import {
  Boxes,
  Calendar,
  ClipboardCheck,
  Droplets,
  MapPin,
  Plus,
} from "lucide-react";
import {
  useEffect,
  useState,
  type FormEvent,
  type ReactNode,
} from "react";
import { useParams } from "react-router-dom";
import {
  createHarvest,
  createInspection,
  getHive,
  listHivePhotos,
  listHarvestsByHive,
  listInspectionsByHive,
  listProducts,
  uploadInspectionPhoto,
} from "../api/hives";
import { HealthBadge } from "../components/badges/HealthBadge";
import { TypeBadge } from "../components/badges/TypeBadge";
import { Card } from "../components/Card";
import {
  Field,
  Select,
  TextArea,
  TextInput,
} from "../components/ui/FormControls";
import { Modal } from "../components/ui/Modal";
import { LoadingState, PageState } from "../components/ui/PageState";
import { useAsync } from "../hooks/useAsync";
import { formatDate } from "../lib/format";
import type {
  Harvest,
  HealthLevel,
  Hive,
  Inspection,
  Product,
} from "../types/hives";

type Tab = "inspections" | "harvests";

interface DetailData {
  hive: Hive;
  inspections: Inspection[];
  harvests: Harvest[];
  products: Product[];
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

async function loadDetail(hiveId: string): Promise<DetailData> {
  const hive = await getHive(hiveId);
  const [inspections, harvests, products] = await Promise.all([
    listInspectionsByHive(hiveId),
    listHarvestsByHive(hiveId),
    listProducts(),
  ]);

  return { hive, inspections, harvests, products };
}
