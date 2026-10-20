import { Boxes, MapPin, Plus, Search, X } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { createHive, listHivePhotos, listHives } from "../api/hives";
import { HealthDot } from "../components/badges/HealthDot";
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
import type { Hive, HiveType } from "../types/hives";

export default function HivesList() {
  const navigate = useNavigate();
  const location = useLocation();
  const routeNotice = (location.state as { notice?: string } | null)?.notice;
  const { data, loading, error, reload } = useAsync(listHives, []);
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");
  const [showModal, setShowModal] = useState(false);

  const hives = useMemo(() => data ?? [], [data]);
  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase();

    return hives.filter((hive) => {
      const matchesSearch =
        hive.name.toLowerCase().includes(query) ||
        hive.species.toLowerCase().includes(query) ||
        (hive.location_description ?? "").toLowerCase().includes(query);
      const matchesType = typeFilter === "all" || hive.type === typeFilter;

      return matchesSearch && matchesType;
    });
  }, [hives, search, typeFilter]);

  return (
    <div className="mx-auto max-w-screen-xl p-5 sm:p-8">
      {routeNotice && (
        <p role="status" className="mb-4 rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
          {routeNotice}
        </p>
      )}
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-neutral-800">Colmeias</h1>
          <p className="mt-1 text-sm text-neutral-500">
            {hives.length} colmeias cadastradas
          </p>
        </div>
        <button
          type="button"
          onClick={() => setShowModal(true)}
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#1D6A4A] px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-[#155438]"
        >
          <Plus size={15} />
          Nova Colmeia
        </button>
      </div>

      <div className="mb-6 flex flex-col gap-3 lg:flex-row lg:items-center">
        <div className="relative w-full max-w-md">
          <Search
            size={14}
            className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400"
          />
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Buscar por nome, espécie ou local..."
            className="w-full rounded-lg border border-neutral-300 bg-white py-2 pl-9 pr-3 text-sm outline-none transition-colors focus:border-[#1D6A4A]"
          />
        </div>

        <Select value={typeFilter} onChange={setTypeFilter}>
          <option value="all">Todos os tipos</option>
          <option value="caixa">Caixa</option>
          <option value="isca">Isca</option>
        </Select>

        {(search || typeFilter !== "all") && (
          <button
            type="button"
            onClick={() => {
              setSearch("");
              setTypeFilter("all");
            }}
            className="inline-flex items-center gap-1 rounded-lg border border-neutral-300 px-2.5 py-2 text-xs text-neutral-500 transition-colors hover:text-neutral-800"
          >
            <X size={12} />
            Limpar
          </button>
        )}
      </div>

      {loading && <LoadingState />}
      {error && (
        <PageState
          title="Não foi possível carregar as colmeias"
          description={error}
          icon={<Boxes size={24} />}
        />
      )}
      {!loading && !error && filtered.length === 0 && (
        <PageState
          title="Nenhuma colmeia encontrada"
          description="Cadastre uma colmeia ou ajuste os filtros para visualizar seus registros."
          icon={<Boxes size={24} />}
        />
      )}
      {!loading && !error && filtered.length > 0 && (
        <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
          {filtered.map((hive) => (
            <HiveCard
              key={hive.id}
              hive={hive}
              onClick={() => navigate(`/hives/${hive.id}`)}
            />
          ))}
        </div>
      )}

      {showModal && (
        <NewHiveModal
          onClose={() => setShowModal(false)}
          onCreated={() => {
            setShowModal(false);
            void reload();
          }}
        />
      )}
    </div>
  );
}

function HiveCard({ hive, onClick }: { hive: Hive; onClick: () => void }) {
  const [photoUrl, setPhotoUrl] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    void listHivePhotos(hive.id)
      .then((photos) => {
        if (!active) {
          return;
        }
        setPhotoUrl(photos[0]?.data_url ?? null);
      })
      .catch(() => {
        if (active) {
          setPhotoUrl(null);
        }
      });

    return () => {
      active = false;
    };
  }, [hive.id]);

  return (
    <button type="button" onClick={onClick} className="text-left">
      <Card className="overflow-hidden transition-shadow hover:shadow-lg">
        <div
          className="relative flex h-40 items-center justify-center overflow-hidden bg-[#e8f3ed]"
          style={{
            backgroundImage: photoUrl ? `url(${photoUrl})` : undefined,
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        >
          {!photoUrl && <Boxes size={44} className="text-[#1D6A4A]" />}
          <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
          <div className="absolute left-3 top-3">
            <TypeBadge type={hive.type} />
          </div>
          <div className="absolute right-3 top-3">
            <HealthDot health="regular" />
          </div>
        </div>
        <div className="p-4">
          <h3 className="text-sm font-semibold text-neutral-800">
            {hive.name}
          </h3>
          <p className="mt-0.5 text-xs italic text-neutral-500">
            {hive.species}
          </p>
          <div className="mt-3 border-t border-[#f0ece4] pt-3 text-xs text-neutral-500">
            <p className="flex items-start gap-1.5">
              <MapPin size={13} className="mt-0.5 shrink-0 text-[#1D6A4A]" />
              {hive.location_description || "Localização não informada"}
            </p>
          </div>
        </div>
      </Card>
    </button>
  );
}

function NewHiveModal({
  onClose,
  onCreated,
}: {
  onClose: () => void;
  onCreated: () => void;
}) {
  const [name, setName] = useState("");
  const [species, setSpecies] = useState("");
  const [type, setType] = useState<HiveType>("caixa");
  const [location, setLocation] = useState("");
  const [notes, setNotes] = useState("");
  const [photoFile, setPhotoFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      await createHive(
        {
          name,
          species,
          type,
          location_description: location || null,
          notes: notes || null,
        },
        photoFile ?? undefined,
      );
      onCreated();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Não foi possível cadastrar.",
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Modal title="Nova Colmeia" onClose={onClose}>
      <form onSubmit={submit} className="space-y-4">
        <Field label="Nome">
          <TextInput
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
          />
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Espécie">
            <TextInput
              value={species}
              onChange={(event) => setSpecies(event.target.value)}
              required
            />
          </Field>
          <Field label="Tipo">
            <Select
              value={type}
              onChange={(value) => setType(value as HiveType)}
              className="w-full"
            >
              <option value="caixa">Caixa</option>
              <option value="isca">Isca</option>
            </Select>
          </Field>
        </div>
        <Field label="Localização">
          <TextInput
            value={location}
            onChange={(event) => setLocation(event.target.value)}
            placeholder="Setor, referência ou descrição"
          />
        </Field>
        <Field label="Notas">
          <TextArea
            value={notes}
            onChange={(event) => setNotes(event.target.value)}
          />
        </Field>
        <Field label="Foto da colmeia (opcional)">
          <input
            type="file"
            accept="image/*"
            onChange={(event) => setPhotoFile(event.target.files?.[0] ?? null)}
            className="block w-full text-sm text-neutral-600 file:mr-3 file:rounded-lg file:border-0 file:bg-[#1D6A4A] file:px-3 file:py-2 file:text-sm file:font-medium file:text-white"
          />
        </Field>
        {error && <p className="text-sm text-red-600">{error}</p>}
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
      </form>
    </Modal>
  );
}
