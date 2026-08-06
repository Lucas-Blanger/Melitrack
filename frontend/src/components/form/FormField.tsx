import { cloneElement, type ReactElement, type ReactNode } from "react";

export function FormField({
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
