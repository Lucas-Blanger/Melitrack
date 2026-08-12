export interface User {
  id: string;
  name: string;
  email: string;
  is_active: boolean;
  created_at: string;
  meliponary_name?: string | null;
  meliponary_location?: string | null;
  inspection_frequency_days?: number | null;
  notify_health_alerts?: boolean | null;
  notify_email?: boolean | null;
  auth_provider?: "local" | "google" | string | null;
  picture?: string | null;
}

export type AuthMode = "login" | "register";
export type RecoveryStep = "email" | "code" | "reset";
export type Notice = { type: "success" | "error"; text: string } | null;
