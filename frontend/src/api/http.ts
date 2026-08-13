import { API_BASE_URL } from "./config";

type JsonBody = object;

async function requestJson<T>(
  path: string,
  options: Omit<RequestInit, "body"> & { body?: BodyInit | JsonBody } = {},
): Promise<T> {
  const headers = new Headers(options.headers);
  const storedToken =
    typeof window !== "undefined"
      ? window.localStorage.getItem("melitrack_token")
      : null;

  if (storedToken) {
    headers.set("Authorization", `Bearer ${storedToken}`);
  }

  let body: BodyInit | undefined;

  if (options.body instanceof FormData || typeof options.body === "string") {
    body = options.body;
  } else if (options.body) {
    headers.set("Content-Type", "application/json");
    body = JSON.stringify(options.body);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: "include",
    ...options,
    headers,
    body,
  });

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    const detail = data?.detail;
    throw new Error(
      typeof detail === "string" ? detail : "Erro ao processar solicitação.",
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export function getJson<T>(path: string) {
  return requestJson<T>(path);
}

export function postJson<T = void>(path: string, body: JsonBody) {
  return requestJson<T>(path, { method: "POST", body });
}

export function postFormData<T = void>(path: string, body: FormData) {
  return requestJson<T>(path, { method: "POST", body });
}

export function putJson<T>(path: string, body: JsonBody) {
  return requestJson<T>(path, { method: "PUT", body });
}

export function patchJson<T>(path: string, body: JsonBody) {
  return requestJson<T>(path, { method: "PATCH", body });
}

export function deleteJson(path: string) {
  return requestJson<void>(path, { method: "DELETE" });
}
