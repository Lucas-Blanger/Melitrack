import {
  Bell,
  Check,
  KeyRound,
  Mail,
  MapPin,
  Save,
  Settings,
  UserRound,
} from "lucide-react";
import { useEffect, useState, type FormEvent, type ReactNode } from "react";
import { changePassword, updateCurrentUser } from "../api/auth";
import { useAuth } from "../auth/AuthContext";
import { Card } from "../components/Card";
import { Field, TextInput } from "../components/ui/FormControls";

type Notice = { type: "success" | "error"; text: string } | null;

export default function SettingsScreen() {
  const { user, refreshUser } = useAuth();
  const [notice, setNotice] = useState<Notice>(null);
  const [passwordNotice, setPasswordNotice] = useState<Notice>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [form, setForm] = useState({
    name: "",
    email: "",
    meliponaryName: "",
    meliponaryLocation: "",
    inspectionFrequencyDays: 14,
    notifyHealthAlerts: true,
    notifyEmail: true,
  });
  const [passwordForm, setPasswordForm] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  });

  useEffect(() => {
    if (!user) return;

    // Keep the editable form in sync when the authenticated user changes.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setForm({
      name: user.name,
      email: user.email,
      meliponaryName: user.meliponary_name ?? "Meu Meliponário",
      meliponaryLocation: user.meliponary_location ?? "",
      inspectionFrequencyDays: user.inspection_frequency_days ?? 14,
      notifyHealthAlerts: user.notify_health_alerts ?? true,
      notifyEmail: user.notify_email ?? true,
    });
  }, [user]);

  const handleSaveSettings = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSaving(true);
    setNotice(null);

    try {
      await updateCurrentUser({
        name: form.name.trim(),
        email: form.email.trim(),
        meliponary_name: form.meliponaryName.trim() || null,
        meliponary_location: form.meliponaryLocation.trim() || null,
        inspection_frequency_days: Math.min(
          365,
          Math.max(1, form.inspectionFrequencyDays),
        ),
        notify_health_alerts: form.notifyHealthAlerts,
        notify_email: form.notifyEmail,
      });
      await refreshUser();
      setNotice({ type: "success", text: "Configurações salvas com sucesso." });
    } catch (error) {
      setNotice({
        type: "error",
        text: error instanceof Error ? error.message : "Não foi possível salvar.",
      });
    } finally {
      setIsSaving(false);
    }
  };

  const handleChangePassword = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsChangingPassword(true);
    setPasswordNotice(null);

    try {
      await changePassword({
        current_password: passwordForm.currentPassword,
        new_password: passwordForm.newPassword,
        confirm_password: passwordForm.confirmPassword,
      });
      setPasswordForm({
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
      });
      setPasswordNotice({ type: "success", text: "Senha atualizada com sucesso." });
    } catch (error) {
      setPasswordNotice({
        type: "error",
        text:
          error instanceof Error
            ? error.message
            : "Não foi possível atualizar a senha.",
      });
    } finally {
      setIsChangingPassword(false);
    }
  };

  const isGoogleAccount = user?.auth_provider === "google";

  return (
    <div className="mx-auto max-w-screen-lg p-5 sm:p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-neutral-800">Configurações</h1>
        <p className="mt-1 text-sm text-neutral-500">
          Perfil, meliponário e preferências da conta
        </p>
      </div>

      <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_340px]">
        <Card className="p-6">
          <form onSubmit={handleSaveSettings} className="space-y-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50 text-[#1D6A4A]">
                <Settings size={20} />
              </div>
              <div>
                <h2 className="text-base font-semibold text-neutral-800">
                  Preferências gerais
                </h2>
                <p className="text-sm text-neutral-500">
                  Esses dados podem ser preenchidos depois do cadastro.
                </p>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <IconField icon={<UserRound size={16} />} label="Nome">
                <TextInput
                  required
                  value={form.name}
                  onChange={(event) =>
                    setForm((current) => ({ ...current, name: event.target.value }))
                  }
                />
              </IconField>

              <IconField icon={<Mail size={16} />} label="E-mail">
                <TextInput
                  required
                  type="email"
                  value={form.email}
                  onChange={(event) =>
                    setForm((current) => ({ ...current, email: event.target.value }))
                  }
                />
              </IconField>

              <IconField icon={<Settings size={16} />} label="Nome do meliponário">
                <TextInput
                  value={form.meliponaryName}
                  onChange={(event) =>
                    setForm((current) => ({
                      ...current,
                      meliponaryName: event.target.value,
                    }))
                  }
                />
              </IconField>

              <IconField icon={<MapPin size={16} />} label="Localização">
                <TextInput
                  value={form.meliponaryLocation}
                  onChange={(event) =>
                    setForm((current) => ({
                      ...current,
                      meliponaryLocation: event.target.value,
                    }))
                  }
                />
              </IconField>
            </div>

            <div className="grid gap-4 border-t border-[#f0ece4] pt-5 sm:grid-cols-[220px_minmax(0,1fr)]">
              <Field label="Frequência de inspeção">
                <div className="flex items-center gap-2">
                  <TextInput
                    required
                    min={1}
                    max={365}
                    type="number"
                    value={form.inspectionFrequencyDays}
                    onChange={(event) =>
                      setForm((current) => ({
                        ...current,
                        inspectionFrequencyDays: Math.min(
                          365,
                          Math.max(1, Number(event.target.value) || 1),
                        ),
                      }))
                    }
                  />
                  <span className="shrink-0 text-sm text-neutral-500">dias</span>
                </div>
              </Field>

              <div className="grid gap-3 sm:grid-cols-2">
                <Toggle
                  checked={form.notifyHealthAlerts}
                  icon={<Bell size={16} />}
                  label="Alertas de saúde"
                  onChange={(checked) =>
                    setForm((current) => ({
                      ...current,
                      notifyHealthAlerts: checked,
                    }))
                  }
                />
                <Toggle
                  checked={form.notifyEmail}
                  icon={<Mail size={16} />}
                  label="Notificações por e-mail"
                  onChange={(checked) =>
                    setForm((current) => ({ ...current, notifyEmail: checked }))
                  }
                />
              </div>
            </div>

            <div className="flex flex-col gap-3 border-t border-[#f0ece4] pt-5 sm:flex-row sm:items-center sm:justify-between">
              {notice && <NoticeMessage notice={notice} />}
              {!notice && <div />}
              <button
                type="submit"
                disabled={isSaving}
                className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#1D6A4A] px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-[#155238] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isSaving ? <Check size={16} /> : <Save size={16} />}
                {isSaving ? "Salvando" : "Salvar configurações"}
              </button>
            </div>
          </form>
        </Card>

        <Card className="p-6">
          <form onSubmit={handleChangePassword} className="space-y-5">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-700">
                <KeyRound size={20} />
              </div>
              <div>
                <h2 className="text-base font-semibold text-neutral-800">Senha</h2>
                <p className="text-sm text-neutral-500">
                  {isGoogleAccount ? "Conta conectada ao Google" : "Acesso local"}
                </p>
              </div>
            </div>

            {isGoogleAccount ? (
              <div className="rounded-lg border border-[#f0ece4] bg-neutral-50 p-4 text-sm leading-relaxed text-neutral-500">
                Esta conta usa autenticação com Google, então a senha é gerenciada fora
                do Melitrack.
              </div>
            ) : (
              <>
                <Field label="Senha atual">
                  <TextInput
                    required
                    minLength={1}
                    type="password"
                    value={passwordForm.currentPassword}
                    onChange={(event) =>
                      setPasswordForm((current) => ({
                        ...current,
                        currentPassword: event.target.value,
                      }))
                    }
                  />
                </Field>
                <Field label="Nova senha">
                  <TextInput
                    required
                    minLength={8}
                    type="password"
                    value={passwordForm.newPassword}
                    onChange={(event) =>
                      setPasswordForm((current) => ({
                        ...current,
                        newPassword: event.target.value,
                      }))
                    }
                  />
                </Field>
                <Field label="Confirmar nova senha">
                  <TextInput
                    required
                    minLength={8}
                    type="password"
                    value={passwordForm.confirmPassword}
                    onChange={(event) =>
                      setPasswordForm((current) => ({
                        ...current,
                        confirmPassword: event.target.value,
                      }))
                    }
                  />
                </Field>

                {passwordNotice && <NoticeMessage notice={passwordNotice} />}

                <button
                  type="submit"
                  disabled={isChangingPassword}
                  className="inline-flex w-full items-center justify-center gap-2 rounded-lg border border-[#1D6A4A] px-4 py-2.5 text-sm font-semibold text-[#1D6A4A] transition-colors hover:bg-emerald-50 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  <KeyRound size={16} />
                  {isChangingPassword ? "Atualizando" : "Atualizar senha"}
                </button>
              </>
            )}
          </form>
        </Card>
      </div>
    </div>
  );
}

function IconField({
  icon,
  label,
  children,
}: {
  icon: ReactNode;
  label: string;
  children: ReactNode;
}) {
  return (
    <Field label={label}>
      <div className="flex items-center gap-2 rounded-lg border border-neutral-300 bg-white px-3 transition-colors focus-within:border-emerald-800">
        <span className="shrink-0 text-neutral-400">{icon}</span>
        <div className="min-w-0 flex-1 [&>input]:border-0 [&>input]:px-0 [&>input]:focus:border-0">
          {children}
        </div>
      </div>
    </Field>
  );
}

function Toggle({
  checked,
  icon,
  label,
  onChange,
}: {
  checked: boolean;
  icon: ReactNode;
  label: string;
  onChange: (checked: boolean) => void;
}) {
  return (
    <label className="flex min-h-14 cursor-pointer items-center justify-between gap-3 rounded-lg border border-[#e8e4dc] bg-white px-3 py-2">
      <span className="flex min-w-0 items-center gap-2 text-sm font-medium text-neutral-700">
        <span className="shrink-0 text-[#1D6A4A]">{icon}</span>
        <span className="min-w-0">{label}</span>
      </span>
      <input
        checked={checked}
        className="h-4 w-4 accent-[#1D6A4A]"
        type="checkbox"
        onChange={(event) => onChange(event.target.checked)}
      />
    </label>
  );
}

function NoticeMessage({ notice }: { notice: Exclude<Notice, null> }) {
  const color =
    notice.type === "success" ? "text-emerald-700" : "text-red-600";

  return <p className={`text-sm font-medium ${color}`}>{notice.text}</p>;
}
