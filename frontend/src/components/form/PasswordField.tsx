import { Eye, EyeOff, Lock } from "lucide-react";

export function PasswordField({
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
