import { Camera, ImageUp, Search } from "lucide-react";
import { useMemo, useState, type FormEvent } from "react";
import { identifyBeeSpecies } from "../api/species";
import { Card } from "../components/Card";
import type { SpeciesIdentificationResponse } from "../types/species";

export default function SpeciesIdentifierScreen() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<SpeciesIdentificationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const previewUrl = useMemo(() => (file ? URL.createObjectURL(file) : null), [file]);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      setError("Selecione uma foto para identificar a espécie.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      setResult(await identifyBeeSpecies(file));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Não foi possível identificar.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-screen-lg p-5 sm:p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-neutral-800">
          Identificar Espécie
        </h1>
        <p className="mt-1 text-sm text-neutral-500">
          Envie uma foto da abelha para estimar a espécie mais provável.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-5">
        <Card className="p-5 lg:col-span-2">
          <form onSubmit={submit} className="space-y-4">
            <label className="flex min-h-56 cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-[#d8d2c7] bg-[#fafaf8] px-4 py-8 text-center transition-colors hover:border-[#1D6A4A] hover:bg-emerald-50/40">
              {previewUrl ? (
                <img
                  src={previewUrl}
                  alt="Prévia da abelha"
                  className="h-48 w-full rounded-lg object-cover"
                />
              ) : (
                <>
                  <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50 text-[#1D6A4A]">
                    <ImageUp size={24} />
                  </div>
                  <p className="text-sm font-semibold text-neutral-700">
                    Selecionar foto
                  </p>
                  <p className="mt-1 text-xs text-neutral-500">
                    JPG, PNG ou WEBP com boa iluminação
                  </p>
                </>
              )}
              <input
                type="file"
                accept="image/*"
                className="sr-only"
                onChange={(event) => {
                  setFile(event.target.files?.[0] ?? null);
                  setResult(null);
                  setError(null);
                }}
              />
            </label>

            {error && <p className="text-sm text-red-600">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#1D6A4A] px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-[#155438] disabled:opacity-60"
            >
              {loading ? (
                <span className="h-4 w-4 rounded-full border-2 border-white border-t-transparent animate-spin" />
              ) : (
                <Search size={15} />
              )}
              {loading ? "Identificando..." : "Identificar espécie"}
            </button>
          </form>
        </Card>

        <Card className="p-5 lg:col-span-3">
          {!result ? (
            <div className="flex min-h-72 flex-col items-center justify-center text-center">
              <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-xl bg-amber-50 text-amber-600">
                <Camera size={26} />
              </div>
              <h2 className="text-base font-semibold text-neutral-800">
                Resultado da identificação
              </h2>
              <p className="mt-2 max-w-sm text-sm leading-relaxed text-neutral-500">
                O resultado aparecerá aqui com a espécie provável, nome científico
                e alternativas mais próximas.
              </p>
            </div>
          ) : (
            <SpeciesResult result={result} />
          )}
        </Card>
      </div>
    </div>
  );
}

function SpeciesResult({ result }: { result: SpeciesIdentificationResponse }) {
  return (
    <div>
      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-neutral-400">
        Espécie provável
      </p>
      <div className="rounded-xl bg-emerald-50 p-5">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <h2 className="text-2xl font-bold text-[#1D6A4A]">
              {result.prediction.label}
            </h2>
            <p className="mt-1 text-sm italic text-neutral-600">
              {result.prediction.scientific_name}
            </p>
          </div>
          <span className="rounded-full bg-white px-3 py-1 text-sm font-semibold text-[#1D6A4A]">
            {Math.round(result.prediction.confidence * 100)}%
          </span>
        </div>
      </div>

      <div className="mt-6">
        <h3 className="mb-3 text-sm font-semibold text-neutral-800">
          Alternativas
        </h3>
        <div className="space-y-3">
          {result.alternatives.map((item) => (
            <div
              key={item.scientific_name}
              className="rounded-xl border border-[#f0ece4] p-4"
            >
              <div className="mb-2 flex items-center justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold text-neutral-800">
                    {item.label}
                  </p>
                  <p className="text-xs italic text-neutral-500">
                    {item.scientific_name}
                  </p>
                </div>
                <span className="text-xs font-semibold text-neutral-500">
                  {Math.round(item.confidence * 100)}%
                </span>
              </div>
              <div className="h-1.5 overflow-hidden rounded-full bg-neutral-100">
                <div
                  className="h-full rounded-full bg-amber-500"
                  style={{ width: `${Math.round(item.confidence * 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
