import { Navigate, Route, Routes, useNavigate } from "react-router-dom";
import Login from "./screens/Login";

export default function App() {
  const navigate = useNavigate();

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route
        path="/login"
        element={
          <Login
            key="login"
            initialMode="login"
            onLogin={() => navigate("/login")}
            onModeChange={(mode) =>
              navigate(mode === "login" ? "/login" : "/register")
            }
          />
        }
      />
      <Route
        path="/register"
        element={
          <Login
            key="register"
            initialMode="register"
            onLogin={() => navigate("/login")}
            onModeChange={(mode) =>
              navigate(mode === "login" ? "/login" : "/register")
            }
          />
        }
      />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
