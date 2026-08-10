import {
  Boxes,
  ChevronLeft,
  ClipboardList,
  Droplets,
  LayoutDashboard,
  LogOut,
  Settings,
} from "lucide-react";
import type { ReactNode } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../auth/AuthContext";
import { HoneycombPattern } from "../HoneycombPattern";
import { MelitrackLogo } from "../MelitrackLogo";

const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/hives", label: "Colmeias", icon: Boxes },
  { to: "/inspections", label: "Inspeções", icon: ClipboardList },
  { to: "/harvests", label: "Colheitas", icon: Droplets },
  { to: "/settings", label: "Configurações", icon: Settings },
];

export function AppShell({
  children,
  backToHives = false,
}: {
  children: ReactNode;
  backToHives?: boolean;
}) {
  const navigate = useNavigate();
  const { user, signOut } = useAuth();
  const initials = user?.name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("") || "MT";

  const logout = async () => {
    await signOut();
    navigate("/login");
  };

  return (
    <div className="flex h-screen overflow-hidden bg-[#F7F5F0]">
      <aside className="hidden w-60 shrink-0 flex-col border-r border-[#e8e4dc] bg-white md:flex">
        <div className="flex items-center gap-2.5 border-b border-[#f0ece4] px-5 py-4">
          <MelitrackLogo size={34} />
          <div className="min-w-0">
            <p className="text-sm font-bold text-[#1D6A4A]">Melitrack</p>
            <p className="text-xs text-neutral-400">Gestão de meliponário</p>
          </div>
        </div>



        <nav className="flex-1 space-y-0.5 overflow-auto p-3">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-[#1D6A4A] text-white"
                    : "text-neutral-600 hover:bg-emerald-50 hover:text-neutral-900"
                }`
              }
            >
              <item.icon size={16} className="shrink-0" />
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="relative h-20 overflow-hidden opacity-20">
          <HoneycombPattern opacity={0.6} />
        </div>

        <div className="border-t border-[#f0ece4] px-4 py-3">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#1D6A4A] text-xs font-bold text-white">
              {initials}
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-xs font-semibold text-neutral-800">
                {user?.name ?? "Usuário Melitrack"}
              </p>
              <p className="truncate text-xs text-neutral-400">
                {user?.email ?? "Sessão ativa"}
              </p>
            </div>
            <button
              type="button"
              onClick={logout}
              className="shrink-0 text-neutral-400 transition-colors hover:text-neutral-700"
              title="Sair"
            >
              <LogOut size={14} />
            </button>
          </div>
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col overflow-hidden">
        <header className="flex h-[52px] shrink-0 items-center gap-4 border-b border-[#e8e4dc] bg-white px-4 sm:px-6">
          {backToHives && (
            <button
              type="button"
              onClick={() => navigate("/hives")}
              className="flex items-center gap-1 text-sm text-neutral-500 transition-colors hover:text-neutral-800"
            >
              <ChevronLeft size={16} />
              Colmeias
            </button>
          )}

          <div className="flex-1" />


        </header>

        <main className="flex-1 overflow-auto">{children}</main>
      </div>
    </div>
  );
}
