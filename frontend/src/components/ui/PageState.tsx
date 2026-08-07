import type { ReactNode } from "react";

interface PageStateProps {
  title: string;
  description?: string;
  icon?: ReactNode;
  action?: ReactNode;
}

export function PageState({ title, description, icon, action }: PageStateProps) {
  return (
    <div className="flex min-h-[320px] flex-col items-center justify-center px-6 py-16 text-center">
      {icon && (
        <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-xl bg-emerald-50 text-emerald-800">
          {icon}
        </div>
      )}
      <h3 className="text-base font-semibold text-neutral-800">{title}</h3>
      {description && (
        <p className="mt-2 max-w-sm text-sm leading-relaxed text-neutral-500">
          {description}
        </p>
      )}
      {action && <div className="mt-5">{action}</div>}
    </div>
  );
}

export function LoadingState({ label = "Carregando dados" }: { label?: string }) {
  return (
    <div className="flex min-h-[320px] items-center justify-center text-sm text-neutral-500">
      {label}
    </div>
  );
}
