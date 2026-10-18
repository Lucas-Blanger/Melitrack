import type { ReactNode } from "react";

interface SelectProps {
  value: string;
  onChange: (value: string) => void;
  children: ReactNode;
  className?: string;
  required?: boolean;
}

export function Select({
  value,
  onChange,
  children,
  className = "",
  required,
}: SelectProps) {
  return (
    <select
      value={value}
      onChange={(event) => onChange(event.target.value)}
      required={required}
      className={`rounded-lg border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-700 outline-none transition-colors focus:border-emerald-800 ${className}`}
    >
      {children}
    </select>
  );
}

export function TextInput(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...props}
      className={`w-full rounded-lg border border-neutral-300 bg-white px-3 py-2 text-sm outline-none transition-colors focus:border-emerald-800 ${props.className ?? ""}`}
    />
  );
}

export function TextArea(props: React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      {...props}
      className={`min-h-24 w-full resize-none rounded-lg border border-neutral-300 bg-white px-3 py-2 text-sm outline-none transition-colors focus:border-emerald-800 ${props.className ?? ""}`}
    />
  );
}

export function Field({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-xs font-medium text-neutral-600">
        {label}
      </span>
      {children}
    </label>
  );
}
