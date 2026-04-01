import { useState } from "react";
import { Menu, X } from "lucide-react";
import { Page } from "../../App";

interface Props {
  onNavigate: (page: Page) => void;
  activePage?: Page;
}

const NAV_LINKS: { label: string; page: Page }[] = [
  { label: "Услуги", page: "services" },
  { label: "Врачи", page: "doctors" },
  { label: "Цены", page: "prices" },
  { label: "Контакты", page: "contacts" },
];

export function Header({ onNavigate, activePage }: Props) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header
      style={{ backgroundColor: "#FFFFFF", borderBottom: "1px solid #E8EEF4" }}
      className="sticky top-0 z-50"
    >
      <div className="max-w-5xl mx-auto px-5 py-4 flex items-center justify-between">
        {/* Logo */}
        <button
          onClick={() => onNavigate("public")}
          className="flex items-center gap-2.5"
        >
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ backgroundColor: "#1B6CA8" }}
          >
            <span style={{ color: "#fff", fontSize: "13px", fontWeight: 700, letterSpacing: "0.5px" }}>A</span>
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: "16px", color: "#1A2B3C", letterSpacing: "0.3px" }}>
              Aster Dental
            </div>
            <div style={{ fontSize: "10px", color: "#6B8FA8", fontWeight: 400, marginTop: "-2px" }}>
              стоматологическая клиника
            </div>
          </div>
        </button>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-1">
          {NAV_LINKS.map((item) => (
            <button
              key={item.page}
              onClick={() => onNavigate(item.page)}
              className="px-4 py-2 rounded-lg transition-all"
              style={{
                color: activePage === item.page ? "#1B6CA8" : "#4A6480",
                backgroundColor: activePage === item.page ? "#EBF4FB" : "transparent",
                fontSize: "14px",
                fontWeight: activePage === item.page ? 600 : 500,
              }}
            >
              {item.label}
            </button>
          ))}
          <div className="w-px h-5 mx-2" style={{ backgroundColor: "#E8EEF4" }} />
          <button
            onClick={() => onNavigate("cabinet")}
            className="px-4 py-2 rounded-lg transition-all"
            style={{ backgroundColor: "#1B6CA8", color: "#fff", fontSize: "14px", fontWeight: 500 }}
          >
            Войти
          </button>
        </nav>

        {/* Mobile toggle */}
        <button
          className="md:hidden p-2 rounded-lg"
          style={{ color: "#1A2B3C" }}
          onClick={() => setMenuOpen(!menuOpen)}
        >
          {menuOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Mobile dropdown */}
      {menuOpen && (
        <div
          className="md:hidden px-5 pb-4 flex flex-col gap-1"
          style={{ borderTop: "1px solid #E8EEF4" }}
        >
          {NAV_LINKS.map((item) => (
            <button
              key={item.page}
              onClick={() => { onNavigate(item.page); setMenuOpen(false); }}
              className="px-3 py-2.5 rounded-lg text-left transition-all"
              style={{
                color: activePage === item.page ? "#1B6CA8" : "#4A6480",
                backgroundColor: activePage === item.page ? "#EBF4FB" : "transparent",
                fontSize: "15px",
                fontWeight: activePage === item.page ? 600 : 400,
              }}
            >
              {item.label}
            </button>
          ))}
          <button
            onClick={() => { onNavigate("cabinet"); setMenuOpen(false); }}
            className="mt-2 px-3 py-2.5 rounded-lg text-left"
            style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "15px", fontWeight: 500 }}
          >
            Войти в кабинет
          </button>
        </div>
      )}
    </header>
  );
}
