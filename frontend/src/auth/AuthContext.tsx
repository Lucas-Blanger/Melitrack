/* eslint-disable react-refresh/only-export-components */
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { clearStoredAuthToken, getCurrentUser, logoutUser } from "../api/auth";
import type { User } from "../types/auth";

type AuthStatus = "checking" | "authenticated" | "guest";

interface AuthContextValue {
  status: AuthStatus;
  user: User | null;
  refreshUser: () => Promise<User | null>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<AuthStatus>("checking");
  const [user, setUser] = useState<User | null>(null);

  const refreshUser = useCallback(async () => {
    try {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
      setStatus("authenticated");
      return currentUser;
    } catch {
      setUser(null);
      setStatus("guest");
      return null;
    }
  }, []);

  const signOut = useCallback(async () => {
    await logoutUser().catch(() => undefined);
    clearStoredAuthToken();
    setUser(null);
    setStatus("guest");
  }, []);

  useEffect(() => {
    // Check the HttpOnly cookie session once when the provider mounts.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void refreshUser();
  }, [refreshUser]);

  const value = useMemo(
    () => ({ status, user, refreshUser, signOut }),
    [status, user, refreshUser, signOut],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }

  return context;
}
