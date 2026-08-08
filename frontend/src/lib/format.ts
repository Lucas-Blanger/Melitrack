export function formatDateTime(value?: string | null) {
  if (!value) return "Sem data";

  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

export function formatDate(value?: string | null) {
  if (!value) return "Sem data";

  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(new Date(value));
}

export function daysSince(value?: string | null) {
  if (!value) return null;

  const inspectedAt = new Date(value).getTime();
  const diff = Date.now() - inspectedAt;
  const days = Math.max(0, Math.floor(diff / 86_400_000));

  if (days === 0) return "hoje";
  if (days === 1) return "há 1 dia";

  return `há ${days} dias`;
}

export function pluralize(count: number, singular: string, plural: string) {
  return count === 1 ? singular : plural;
}
