import { getJson, postJson, putJson } from "./http";
import type { User } from "../types/auth";

export function registerUser(body: {
  name: string;
  email: string;
  password: string;
}) {
  return postJson("/auth/register", body);
}

export function loginUser(body: { email: string; password: string }) {
  return postJson("/auth/login", body);
}

export function getCurrentUser() {
  return getJson<User>("/auth/me");
}

export function updateCurrentUser(body: {
  name?: string;
  email?: string;
  meliponary_name?: string | null;
  meliponary_location?: string | null;
  inspection_frequency_days?: number;
  notify_health_alerts?: boolean;
  notify_email?: boolean;
}) {
  return putJson<User>("/auth/me", body);
}

export function changePassword(body: {
  current_password: string;
  new_password: string;
  confirm_password: string;
}) {
  return postJson<void>("/auth/change-password", body);
}

export function logoutUser() {
  clearStoredAuthToken();
  return postJson("/auth/logout", {});
}

export function requestPasswordReset(body: { email: string }) {
  return postJson("/auth/forgot-password", body);
}

export function verifyResetCode(body: { email: string; code: string }) {
  return postJson("/auth/verify-reset-code", body);
}

export function resetPassword(body: {
  email: string;
  code: string;
  new_password: string;
  confirm_password: string;
}) {
  return postJson("/auth/reset-password", body);
}

export function clearStoredAuthToken() {
  window.localStorage.removeItem("melitrack_token");
}
