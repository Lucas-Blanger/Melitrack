import type { AuthMode } from "../../types/auth";

export function AuthModeTabs({
  mode,
  onChange,
}: {
  mode: AuthMode;
  onChange: (mode: AuthMode) => void;
}) {
  return (
    <div
      className="flex rounded-lg p-1 mb-6"
      style={{ backgroundColor: "#f2f0ec" }}
    >
      {(["login", "register"] as const).map((item) => (
        <button
          key={item}
          type="button"
          onClick={() => onChange(item)}
          className="flex-1 py-2 text-sm font-medium rounded-md transition-all"
          style={{
            backgroundColor: mode === item ? "white" : "transparent",
            color: mode === item ? "#1D6A4A" : "#777",
            boxShadow: mode === item ? "0 1px 6px rgba(0,0,0,0.10)" : "none",
          }}
        >
          {item === "login" ? "Entrar" : "Cadastrar"}
        </button>
      ))}
    </div>
  );
}
