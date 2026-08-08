export interface User {
  id: string;
  name: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

export type AuthMode = "login" | "register";
export type RecoveryStep = "email" | "code" | "reset";
export type Notice = { type: "success" | "error"; text: string } | null;
