import {
  cloneElement,
  useState,
  type ReactElement,
  type FormEvent,
  type ReactNode,
} from "react";
import { useLocation } from "react-router-dom";
import {
  ArrowLeft,
  CheckCircle2,
  Eye,
  EyeOff,
  KeyRound,
  Lock,
  Mail,
  User,
} from "lucide-react";
import { HoneycombPattern, MelitrackLogo } from "../components/shared";
import {
  loginUser,
  registerUser,
  requestPasswordReset,
  resetPassword,
  verifyResetCode,
} from "../api/auth";

import { TermsModal } from "../components/TermsModal";

type AuthMode = "login" | "register";
type RecoveryStep = "email" | "code" | "reset";
type Notice = { type: "success" | "error"; text: string } | null;

interface LoginProps {
  initialMode?: AuthMode;
  onLogin: () => void | Promise<void>;
  onModeChange?: (mode: AuthMode) => void;
}

export default function Login({
  initialMode = "login",
  onLogin,
  onModeChange,
}: LoginProps) {
  const location = useLocation();
  const routeNotice = (location.state as { notice?: string } | null)?.notice;
  const [mode, setMode] = useState<AuthMode>(initialMode);
  const [recoveryStep, setRecoveryStep] = useState<RecoveryStep | null>(null);
  const [showPass, setShowPass] = useState(false);
  const [showConfirmPass, setShowConfirmPass] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [acceptedTerms, setAcceptedTerms] = useState(false);
  const [showTermsModal, setShowTermsModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [notice, setNotice] = useState<Notice>(
    routeNotice ? { type: "error", text: routeNotice } : null,
  );

  const title = recoveryStep
    ? "Recuperar senha"
    : mode === "login"
      ? "Entrar"
      : "Criar conta";

  const subtitle = recoveryStep
    ? "Use o código enviado por e-mail"
    : "Gerencie seu meliponário com inteligência";

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setNotice(null);
    setLoading(true);

    try {
      if (recoveryStep) {
        await handleRecoverySubmit();
        return;
      }

      if (mode === "register" && password !== confirmPassword) {
        throw new Error("As senhas não conferem.");
      }

      if (mode === "register") {
        if (!name.trim()) {
          throw new Error("Informe seu nome completo.");
        }

        if (!acceptedTerms) {
          throw new Error("Você precisa ler e aceitar os Termos de Serviço para se cadastrar.");
        }

        await registerUser({ name: name.trim(), email, password });
      }

      await loginUser({ email, password });

      setNotice({
        type: "success",
        text:
          mode === "login" ? "Login realizado." : "Conta criada com sucesso.",
      });
      await onLogin();
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setLoading(false);
    }
  };

  const handleRecoverySubmit = async () => {
    if (recoveryStep === "email") {
      await requestPasswordReset({ email });
      setRecoveryStep("code");
      setNotice({
        type: "success",
        text: "Se o e-mail existir, o código de recuperação foi enviado.",
      });
      return;
    }

    if (recoveryStep === "code") {
      await verifyResetCode({ email, code });
      setRecoveryStep("reset");
      setNotice({ type: "success", text: "Código validado." });
      return;
    }

    await resetPassword({
      email,
      code,
      new_password: password,
      confirm_password: confirmPassword,
    });

    setMode("login");
    setRecoveryStep(null);
    setPassword("");
    setConfirmPassword("");
    setCode("");
    setNotice({
      type: "success",
      text: "Senha atualizada. Entre com sua nova senha.",
    });
    onModeChange?.("login");
  };

  const changeMode = (nextMode: AuthMode) => {
    setMode(nextMode);
    setRecoveryStep(null);
    setNotice(null);
    setPassword("");
    setConfirmPassword("");
    setCode("");
    onModeChange?.(nextMode);
  };

  const startRecovery = () => {
    setRecoveryStep("email");
    setNotice(null);
    setPassword("");
    setConfirmPassword("");
    setCode("");
  };

  const stopRecovery = () => {
    setRecoveryStep(null);
    setNotice(null);
    setPassword("");
    setConfirmPassword("");
    setCode("");
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center relative overflow-hidden px-4 py-8"
      style={{ backgroundColor: "#F7F5F0" }}
    >
      <HoneycombPattern opacity={0.08} />

      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_50%_45%,rgba(29,106,74,0.08),transparent_38%),radial-gradient(circle_at_82%_25%,rgba(232,160,32,0.08),transparent_26%)]" />

      <div className="relative z-10 w-full max-w-md">
        <div
          className="bg-white rounded-xl p-6 sm:p-8"
          style={{
            boxShadow:
              "0 8px 48px rgba(29,106,74,0.10), 0 2px 8px rgba(0,0,0,0.06)",
          }}
        >
          <div className="flex flex-col items-center mb-7">
            <MelitrackLogo size={76} />
            <h1 className="text-xl font-bold mt-4" style={{ color: "#1D6A4A" }}>
              {title}
            </h1>
            <p className="text-sm text-neutral-500 text-center mt-1.5 leading-relaxed">
              {subtitle}
            </p>
          </div>

          {!recoveryStep && (
            <div
              className="flex rounded-lg p-1 mb-6"
              style={{ backgroundColor: "#f2f0ec" }}
            >
              {(["login", "register"] as const).map((item) => (
                <button
                  key={item}
                  type="button"
                  onClick={() => changeMode(item)}
                  className="flex-1 py-2 text-sm font-medium rounded-md transition-all"
                  style={{
                    backgroundColor: mode === item ? "white" : "transparent",
                    color: mode === item ? "#1D6A4A" : "#777",
                    boxShadow:
                      mode === item ? "0 1px 6px rgba(0,0,0,0.10)" : "none",
                  }}
                >
                  {item === "login" ? "Entrar" : "Cadastrar"}
                </button>
              ))}
            </div>
          )}

          {recoveryStep && (
            <button
              type="button"
              onClick={stopRecovery}
              className="mb-5 inline-flex items-center gap-2 text-xs font-medium text-neutral-500 transition-colors hover:text-neutral-800"
            >
              <ArrowLeft size={14} />
              Voltar para login
            </button>
          )}

          {notice && (
            <div
              className="mb-4 flex items-start gap-2 rounded-lg border px-3 py-2.5 text-sm"
              style={{
                backgroundColor:
                  notice.type === "success" ? "#f0fdf4" : "#fef2f2",
                borderColor: notice.type === "success" ? "#bbf7d0" : "#fecaca",
                color: notice.type === "success" ? "#166534" : "#991b1b",
              }}
              role="status"
            >
              {notice.type === "success" ? (
                <CheckCircle2 className="mt-0.5 flex-shrink-0" size={15} />
              ) : (
                <KeyRound className="mt-0.5 flex-shrink-0" size={15} />
              )}
              <span>{notice.text}</span>
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSubmit}>
            {!recoveryStep && mode === "register" && (
              <FormField label="Nome completo" icon={<User size={14} />}>
                <input
                  type="text"
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  placeholder="João Mello"
                  autoComplete="name"
                  required
                />
              </FormField>
            )}

            <FormField label="E-mail" icon={<Mail size={14} />}>
              <input
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="joao@exemplo.com.br"
                autoComplete="email"
                required
              />
            </FormField>

            {(recoveryStep === "code" || recoveryStep === "reset") && (
              <FormField
                label="Código de recuperação"
                icon={<KeyRound size={14} />}
              >
                <input
                  type="text"
                  inputMode="numeric"
                  value={code}
                  onChange={(event) =>
                    setCode(event.target.value.replace(/\D/g, "").slice(0, 6))
                  }
                  placeholder="123456"
                  minLength={6}
                  maxLength={6}
                  required
                />
              </FormField>
            )}

            {(!recoveryStep || recoveryStep === "reset") && (
              <PasswordField
                label={recoveryStep === "reset" ? "Nova senha" : "Senha"}
                value={password}
                show={showPass}
                onToggle={() => setShowPass((current) => !current)}
                onChange={setPassword}
                autoComplete={
                  mode === "login" && !recoveryStep
                    ? "current-password"
                    : "new-password"
                }
              />
            )}

            {(mode === "register" || recoveryStep === "reset") && (
              <PasswordField
                label={
                  recoveryStep === "reset"
                    ? "Confirmar nova senha"
                    : "Confirmar senha"
                }
                value={confirmPassword}
                show={showConfirmPass}
                onToggle={() => setShowConfirmPass((current) => !current)}
                onChange={setConfirmPassword}
                autoComplete="new-password"
              />
            )}

            {!recoveryStep && mode === "login" && (
              <div className="flex justify-end -mt-1">
                <button
                  type="button"
                  onClick={startRecovery}
                  className="text-xs text-neutral-500 transition-colors hover:text-neutral-700"
                >
                  Esqueceu a senha?
                </button>
              </div>
            )}

            {!recoveryStep && mode === "register" && (
              <div className="flex items-start gap-2.5 pt-1 pb-1">
                <input
                  type="checkbox"
                  id="accept-terms"
                  checked={acceptedTerms}
                  onChange={(event) => setAcceptedTerms(event.target.checked)}
                  className="mt-0.5 h-4 w-4 shrink-0 rounded border-neutral-300 text-[#1D6A4A] focus:ring-[#1D6A4A] cursor-pointer"
                  required
                />
                <label htmlFor="accept-terms" className="text-xs text-neutral-600 leading-snug cursor-pointer select-none">
                  Li e aceito os{" "}
                  <button
                    type="button"
                    onClick={() => setShowTermsModal(true)}
                    className="font-semibold text-[#1D6A4A] underline hover:text-[#155438]"
                  >
                    Termos de Serviço
                  </button>{" "}
                  (incluindo a autorização de uso de fotos enviadas para treinamento da IA do sistema).
                </label>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 text-sm font-semibold text-white rounded-lg transition-all mt-1 flex items-center justify-center gap-2 disabled:cursor-not-allowed disabled:opacity-70 hover:bg-[#155438]"
              style={{ backgroundColor: "#1D6A4A" }}
            >
              {loading && (
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              )}
              {getSubmitLabel(mode, recoveryStep)}
            </button>
          </form>
        </div>

        <div className="flex flex-col items-center mt-5 gap-2 text-center text-xs text-neutral-500">
          <p>
            Desenvolvido por{" "}
            <a
              href="https://www.linkedin.com/in/lucas-blanger-4668a2210/"
              target="_blank"
              rel="noopener noreferrer"
              className="font-semibold text-[#1D6A4A] hover:underline"
            >
              Lucas Blanger
            </a>
          </p>
          <button
            type="button"
            onClick={() => setShowTermsModal(true)}
            className="text-neutral-500 hover:text-[#1D6A4A] underline transition-colors"
          >
            Termos de Serviço
          </button>
          <div className="flex justify-center mt-1 gap-1.5">
            {[0.35, 0.55, 0.75].map((opacity) => (
              <div
                key={opacity}
                className="w-1.5 h-1.5 rounded-full"
                style={{ backgroundColor: "#E8A020", opacity }}
              />
            ))}
          </div>
        </div>
      </div>

      <TermsModal isOpen={showTermsModal} onClose={() => setShowTermsModal(false)} />
    </div>
  );
}

function PasswordField({
  label,
  value,
  show,
  autoComplete,
  onToggle,
  onChange,
}: {
  label: string;
  value: string;
  show: boolean;
  autoComplete: string;
  onToggle: () => void;
  onChange: (value: string) => void;
}) {
  return (
    <div>
      <label className="block text-xs font-medium text-neutral-600 mb-1.5">
        {label}
      </label>
      <div
        className="flex items-center rounded-lg border px-3 gap-2 transition-colors focus-within:border-[#1D6A4A]"
        style={{ borderColor: "#ddd", backgroundColor: "#fafaf9" }}
      >
        <span className="text-neutral-400 flex-shrink-0">
          <Lock size={14} />
        </span>
        <input
          type={show ? "text" : "password"}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder="********"
          minLength={8}
          autoComplete={autoComplete}
          required
          className="flex-1 py-2.5 text-sm bg-transparent outline-none text-neutral-800 placeholder:text-neutral-400"
        />
        <button
          type="button"
          onClick={onToggle}
          className="text-neutral-400 transition-colors hover:text-neutral-600"
          aria-label={show ? "Ocultar senha" : "Mostrar senha"}
        >
          {show ? <EyeOff size={14} /> : <Eye size={14} />}
        </button>
      </div>
    </div>
  );
}

function FormField({
  label,
  icon,
  children,
}: {
  label: string;
  icon: ReactNode;
  children: ReactElement<HTMLInputElement>;
}) {
  return (
    <div>
      <label className="block text-xs font-medium text-neutral-600 mb-1.5">
        {label}
      </label>
      <div
        className="flex items-center rounded-lg border px-3 gap-2 transition-colors focus-within:border-[#1D6A4A]"
        style={{ borderColor: "#ddd", backgroundColor: "#fafaf9" }}
      >
        <span className="text-neutral-400 flex-shrink-0">{icon}</span>
        <div className="flex-1">
          {cloneElement(children, {
            className:
              "w-full py-2.5 text-sm bg-transparent outline-none text-neutral-800 placeholder:text-neutral-400",
          })}
        </div>
      </div>
    </div>
  );
}

function getSubmitLabel(mode: AuthMode, recoveryStep: RecoveryStep | null) {
  if (recoveryStep === "email") return "Enviar código";
  if (recoveryStep === "code") return "Validar código";
  if (recoveryStep === "reset") return "Atualizar senha";
  return mode === "login" ? "Entrar na conta" : "Criar conta gratuita";
}

function getErrorMessage(error: unknown) {
  if (error instanceof Error) {
    if (error.message === "Email already registered") {
      return "Este e-mail já está cadastrado.";
    }
    if (error.message === "This account uses Google authentication") {
      return "Esta conta foi criada com o Google. Entre usando esse método.";
    }
    return error.message;
  }
  return "Erro ao processar solicitação.";
}
