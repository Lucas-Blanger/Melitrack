import {
  Boxes,
  ChevronLeft,
  ClipboardList,
  Droplets,
  LayoutDashboard,
  LogOut,
  Menu,
  Search,
  Settings,
  X,
} from "lucide-react";
import type { ReactNode } from "react";
import { useEffect, useRef, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../auth/AuthContext";
import { HoneycombPattern } from "../HoneycombPattern";
import { MelitrackLogo } from "../MelitrackLogo";
import { Footer } from "./Footer";

const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/hives", label: "Colmeias", icon: Boxes },
  { to: "/inspections", label: "Inspeções", icon: ClipboardList },
  { to: "/harvests", label: "Colheitas", icon: Droplets },
  { to: "/species", label: "Espécies", icon: Search },
  { to: "/settings", label: "Configurações", icon: Settings },
];

function SidebarContent({ onNav }: { onNav?: () => void }) {
  const navigate = useNavigate();
  const { user, signOut } = useAuth();
  const initials =
    user?.name
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
    <>
      {/* Logo */}
      <div className="flex items-center gap-2.5 border-b border-[#f0ece4] px-5 py-4">
        <MelitrackLogo size={34} />
        <div className="min-w-0">
          <p className="text-sm font-bold text-[#1D6A4A]">Melitrack</p>
          <p className="text-xs text-neutral-400">Gestão de meliponário</p>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 space-y-0.5 overflow-auto p-3">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            onClick={onNav}
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

      {/* Decorative */}
      <div className="relative h-20 overflow-hidden opacity-20">
        <HoneycombPattern opacity={0.6} />
      </div>

      {/* User footer */}
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
    </>
  );
}

export function AppShell({
  children,
  backToHives = false,
}: {
  children: ReactNode;
  backToHives?: boolean;
}) {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [drawerOpen, setDrawerOpen] = useState(false);
  const drawerRef = useRef<HTMLDivElement>(null);

  const meliponaryName = user?.meliponary_name?.trim() || "Meu Meliponário";

  // Close drawer on outside click
  useEffect(() => {
    if (!drawerOpen) return;
    const handleClick = (e: MouseEvent) => {
      if (drawerRef.current && !drawerRef.current.contains(e.target as Node)) {
        setDrawerOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [drawerOpen]);

  // Prevent body scroll when drawer is open
  useEffect(() => {
    if (drawerOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [drawerOpen]);

  return (
    <div className="flex h-screen overflow-hidden bg-[#F7F5F0]">
      {/* ── Desktop Sidebar ── */}
      <aside className="hidden w-60 shrink-0 flex-col border-r border-[#e8e4dc] bg-white md:flex">
        <SidebarContent />
      </aside>

      {/* ── Mobile Drawer Overlay ── */}
      {drawerOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/40 md:hidden"
          aria-hidden="true"
        />
      )}

      {/* ── Mobile Drawer Panel ── */}
      <div
        ref={drawerRef}
        className={`fixed inset-y-0 left-0 z-50 flex w-72 flex-col bg-white shadow-2xl transition-transform duration-300 ease-in-out md:hidden ${
          drawerOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Close button inside drawer */}
        <button
          type="button"
          onClick={() => setDrawerOpen(false)}
          className="absolute right-3 top-3.5 z-10 rounded-md p-1.5 text-neutral-400 hover:bg-neutral-100 hover:text-neutral-700"
          aria-label="Fechar menu"
        >
          <X size={18} />
        </button>

        <SidebarContent onNav={() => setDrawerOpen(false)} />
      </div>

      {/* ── Main content area ── */}
      <div className="flex min-w-0 flex-1 flex-col overflow-hidden">
        {/* Header */}
        <header className="flex h-[52px] shrink-0 items-center gap-3 border-b border-[#e8e4dc] bg-white px-4 sm:px-6">
          {/* Hamburger – mobile only */}
          <button
            type="button"
            onClick={() => setDrawerOpen(true)}
            className="shrink-0 rounded-md p-1.5 text-neutral-500 transition-colors hover:bg-neutral-100 hover:text-neutral-800 md:hidden"
            aria-label="Abrir menu"
          >
            <Menu size={20} />
          </button>

          {backToHives && (
            <button
              type="button"
              onClick={() => navigate("/hives")}
              className="flex items-center gap-1 text-sm text-neutral-500 transition-colors hover:text-neutral-800"
            >
              <ChevronLeft size={16} />
              <span className="hidden sm:inline">Colmeias</span>
            </button>
          )}

          <div className="flex-1" />

          <div className="min-w-0 text-right">
            <p className="truncate text-sm font-semibold text-[#1D6A4A]">
              {meliponaryName}
            </p>
          </div>
        </header>

        {/* Page content */}
        <main className="flex flex-1 flex-col overflow-auto">
          <div className="flex-1">{children}</div>
          <Footer />
        </main>
      </div>
    </div>
  );
}
