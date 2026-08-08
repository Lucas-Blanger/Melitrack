import { Droplets, Plus } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { getHarvestSummary, listHarvestsByHive, listHives, listProducts } from "../api/hives";
import { Card } from "../components/Card";
import { LoadingState, PageState } from "../components/ui/PageState";
import { useAsync } from "../hooks/useAsync";
import { formatDate } from "../lib/format";
import type { Harvest, HarvestSummary, Hive, Product } from "../types/hives";

interface HarvestData {
  rows: Array<{ hive: Hive; harvest: Harvest }>;
  products: Product[];
  summary: HarvestSummary;
}

export default function HarvestsScreen() {
  const navigate = useNavigate();
  const { data, loading, error } = useAsync(loadHarvests, []);

  if (loading) return <LoadingState />;
  if (error || !data) {
    return (
      <PageState
        title="Não foi possível carregar as colheitas"
        description={error ?? "Tente novamente em instantes."}
        icon={<Droplets size={24} />}
      />
    );
  }

  const productName = (id: number) =>
    data.products.find((product) => product.id === id)?.name ?? `Produto ${id}`;

  return (
    <div className="mx-auto max-w-screen-xl p-5 sm:p-8">
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-neutral-800">Colheitas</h1>
          <p className="mt-1 text-sm text-neutral-500">
            Produção registrada por colmeia e produto
          </p>
        </div>
        <button
          type="button"
          onClick={() => navigate("/hives")}
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#1D6A4A] px-4 py-2.5 text-sm font-medium text-white"
        >
          <Plus size={15} />
          Nova Colheita
        </button>
      </div>

      {data.summary.items.length > 0 && (
        <div className="mb-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {data.summary.items.map((item) => (
            <Card key={`${item.product}-${item.unit}`} className="p-5">
              <p className="text-xs font-medium text-neutral-500">{item.product}</p>
              <p className="mt-2 text-2xl font-bold text-neutral-800">
                {item.total_quantity.toLocaleString("pt-BR")} {item.unit}
              </p>
            </Card>
          ))}
        </div>
      )}

      {data.rows.length === 0 ? (
        <PageState
          title="Nenhuma colheita registrada"
          description="Abra uma colmeia para registrar a primeira colheita."
          icon={<Droplets size={24} />}
        />
      ) : (
        <Card className="overflow-hidden">
          <table className="w-full text-sm">
            <thead className="border-b border-[#e8e4dc] bg-[#fafaf8] text-left text-xs text-neutral-500">
              <tr>
                <th className="px-4 py-3 font-medium">Colmeia</th>
                <th className="px-4 py-3 font-medium">Produto</th>
                <th className="px-4 py-3 font-medium">Quantidade</th>
                <th className="px-4 py-3 font-medium">Data</th>
                <th className="px-4 py-3 font-medium">Notas</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#f0ece4]">
              {data.rows.map(({ hive, harvest }) => (
                <tr
                  key={harvest.id}
                  className="cursor-pointer transition-colors hover:bg-[#fafaf8]"
                  onClick={() => navigate(`/hives/${hive.id}`)}
                >
                  <td className="px-4 py-3 font-medium text-neutral-800">
                    {hive.name}
                  </td>
                  <td className="px-4 py-3 text-neutral-600">
                    {productName(harvest.product_id)}
                  </td>
                  <td className="px-4 py-3 text-neutral-600">
                    {harvest.quantity} {harvest.unit}
                  </td>
                  <td className="px-4 py-3 text-neutral-600">
                    {formatDate(harvest.harvested_at)}
                  </td>
                  <td className="max-w-sm px-4 py-3 text-neutral-500">
                    {harvest.quality_notes || "Sem notas"}
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

async function loadHarvests(): Promise<HarvestData> {
  const [hives, products, summary] = await Promise.all([
    listHives(),
    listProducts(),
    getHarvestSummary(),
  ]);
  const groups = await Promise.all(
    hives.map(async (hive) => ({
      hive,
      harvests: await listHarvestsByHive(hive.id).catch(() => []),
    })),
  );

  return {
    products,
    summary,
    rows: groups
      .flatMap(({ hive, harvests }) =>
        harvests.map((harvest) => ({ hive, harvest })),
      )
      .sort(
        (a, b) =>
          new Date(b.harvest.harvested_at).getTime() -
          new Date(a.harvest.harvested_at).getTime(),
      ),
  };
}
