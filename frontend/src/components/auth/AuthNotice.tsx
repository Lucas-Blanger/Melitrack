import { CheckCircle2, KeyRound } from "lucide-react";
import type { Notice } from "../../types/auth";

export function AuthNotice({ notice }: { notice: Notice }) {
  if (!notice) return null;

  return (
    <div
      className="mb-4 flex items-start gap-2 rounded-lg border px-3 py-2.5 text-sm"
      style={{
        backgroundColor: notice.type === "success" ? "#f0fdf4" : "#fef2f2",
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
  );
}
