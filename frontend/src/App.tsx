import {
  Navigate,
  Route,
  Routes,
  useLocation,
  useNavigate,
} from "react-router-dom";
import type { ReactNode } from "react";
import { useAuth } from "./auth/AuthContext";
import { AppShell } from "./components/layout/AppShell";
import Dashboard from "./screens/Dashboard";
import HarvestsScreen from "./screens/HarvestsScreen";
import HiveDetail from "./screens/HiveDetail";
import HivesList from "./screens/HivesList";
import InspectionsScreen from "./screens/InspectionsScreen";
import Login from "./screens/Login";
import SettingsScreen from "./screens/SettingsScreen";
import SpeciesIdentifierScreen from "./screens/SpeciesIdentifierScreen";

export default function App() {
  const navigate = useNavigate();
  const { refreshUser } = useAuth();

  const handleLogin = async () => {
    await refreshUser();
    navigate("/dashboard");
  };

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route
        path="/login"
        element={
          <PublicAuthRoute>
            <Login
              key="login"
              initialMode="login"
              onLogin={handleLogin}
              onModeChange={(mode) =>
                navigate(mode === "login" ? "/login" : "/register")
              }
            />
          </PublicAuthRoute>
        }
      />
      <Route
        path="/register"
        element={
          <PublicAuthRoute>
            <Login
              key="register"
              initialMode="register"
              onLogin={handleLogin}
              onModeChange={(mode) =>
                navigate(mode === "login" ? "/login" : "/register")
              }
            />
          </PublicAuthRoute>
        }
      />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <AppShell>
              <Dashboard />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/hives"
        element={
          <ProtectedRoute>
            <AppShell>
              <HivesList />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/hives/:hiveId"
        element={
          <ProtectedRoute>
            <AppShell backToHives>
              <HiveDetail />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/inspections"
        element={
          <ProtectedRoute>
            <AppShell>
              <InspectionsScreen />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/harvests"
        element={
          <ProtectedRoute>
            <AppShell>
              <HarvestsScreen />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/species"
        element={
          <ProtectedRoute>
            <AppShell>
              <SpeciesIdentifierScreen />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <AppShell>
              <SettingsScreen />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

function ProtectedRoute({ children }: { children: ReactNode }) {
  const location = useLocation();
  const { status } = useAuth();

  if (status === "checking") {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#F7F5F0] text-sm text-neutral-500">
        Verificando sessão
      </div>
    );
  }

  if (status === "guest") {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return children;
}

function PublicAuthRoute({ children }: { children: ReactNode }) {
  const { status } = useAuth();

  if (status === "checking") {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#F7F5F0] text-sm text-neutral-500">
        Verificando sessão
      </div>
    );
  }

  if (status === "authenticated") {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}
