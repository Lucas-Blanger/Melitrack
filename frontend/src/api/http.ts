import { API_BASE_URL } from "./config";

export async function postJson(path: string, body: Record<string, unknown>) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    const detail = data?.detail;
    throw new Error(
      typeof detail === "string" ? detail : "Erro ao processar solicitação.",
    );
  }
}
