export type AuthMode = "login" | "register";
export type RecoveryStep = "email" | "code" | "reset";
export type Notice = { type: "success" | "error"; text: string } | null;
