import { API_BASE_URL } from "./config";
import { postJson } from "./http";

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

export function redirectToGoogleAuth() {
  const redirectTo = `${window.location.origin}/login`;
  window.location.assign(
    `${API_BASE_URL}/auth/google?redirect_to=${encodeURIComponent(redirectTo)}`,
  );
}
