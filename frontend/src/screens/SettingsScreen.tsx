import { Settings } from "lucide-react";
import { Card } from "../components/Card";

export default function SettingsScreen() {
  return (
    <div className="mx-auto max-w-screen-lg p-5 sm:p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-neutral-800">Configurações</h1>
        <p className="mt-1 text-sm text-neutral-500">
          Preferências e integrações do meliponário
        </p>
      </div>

      <Card className="p-6">
        <div className="mb-5 flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50 text-[#1D6A4A]">
          <Settings size={20} />
        </div>
        <h2 className="text-base font-semibold text-neutral-800">
          Configurações em preparação
        </h2>
        <p className="mt-2 max-w-xl text-sm leading-relaxed text-neutral-500">
          Esta área está pronta para receber preferências da conta, dados do
          meliponário e integrações quando os endpoints correspondentes forem
          adicionados ao backend.
        </p>
      </Card>
    </div>
  );
}
