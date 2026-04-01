import { MapPin, Phone, Mail, MessageCircle, Instagram } from "lucide-react";
import { Page } from "../../App";

interface Props {
  onNavigate: (page: Page) => void;
}

export function Footer({ onNavigate }: Props) {
  return (
    <footer style={{ backgroundColor: "#1A2B3C" }}>
      <div className="max-w-5xl mx-auto px-5 py-10">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="md:col-span-1">
            <button onClick={() => onNavigate("public")} className="flex items-center gap-2.5 mb-3">
              <div
                className="w-8 h-8 rounded-lg flex items-center justify-center"
                style={{ backgroundColor: "#2A5A8A" }}
              >
                <span style={{ color: "#fff", fontSize: "13px", fontWeight: 700 }}>A</span>
              </div>
              <div style={{ fontWeight: 700, fontSize: "16px", color: "#FFFFFF" }}>Aster Dental</div>
            </button>
            <p style={{ fontSize: "13px", color: "#7AAECA", lineHeight: 1.7 }}>
              Современная стоматология с заботой о каждом пациенте.
            </p>
            <div className="flex gap-3 mt-4">
              {[
                { icon: <MessageCircle size={16} />, label: "WhatsApp" },
                { icon: <Instagram size={16} />, label: "Instagram" },
              ].map((s, i) => (
                <a
                  key={i}
                  href="#"
                  className="w-8 h-8 rounded-lg flex items-center justify-center"
                  style={{ backgroundColor: "rgba(255,255,255,0.08)", color: "#7AAECA" }}
                  title={s.label}
                >
                  {s.icon}
                </a>
              ))}
            </div>
          </div>

          {/* Links */}
          <div>
            <div style={{ fontSize: "13px", fontWeight: 600, color: "#FFFFFF", marginBottom: "14px" }}>
              Разделы
            </div>
            <div className="flex flex-col gap-2.5">
              {[
                { label: "Услуги", page: "services" as Page },
                { label: "Врачи", page: "doctors" as Page },
                { label: "Цены", page: "prices" as Page },
                { label: "Контакты", page: "contacts" as Page },
              ].map((l) => (
                <button
                  key={l.page}
                  onClick={() => onNavigate(l.page)}
                  className="text-left"
                  style={{ fontSize: "13px", color: "#7AAECA" }}
                >
                  {l.label}
                </button>
              ))}
            </div>
          </div>

          {/* Contacts */}
          <div>
            <div style={{ fontSize: "13px", fontWeight: 600, color: "#FFFFFF", marginBottom: "14px" }}>
              Контакты
            </div>
            <div className="flex flex-col gap-3">
              <a href="tel:+78001234567" className="flex items-center gap-2.5" style={{ color: "#7AAECA", fontSize: "13px" }}>
                <Phone size={14} />+7 (800) 123-45-67
              </a>
              <a href="mailto:info@asterdental.ru" className="flex items-center gap-2.5" style={{ color: "#7AAECA", fontSize: "13px" }}>
                <Mail size={14} />info@asterdental.ru
              </a>
              <a href="https://wa.me/78001234567" className="flex items-center gap-2.5" style={{ color: "#7AAECA", fontSize: "13px" }}>
                <MessageCircle size={14} />WhatsApp
              </a>
            </div>
          </div>

          {/* Address */}
          <div>
            <div style={{ fontSize: "13px", fontWeight: 600, color: "#FFFFFF", marginBottom: "14px" }}>
              Адрес
            </div>
            <div className="flex items-start gap-2.5" style={{ color: "#7AAECA", fontSize: "13px" }}>
              <MapPin size={14} className="mt-0.5 shrink-0" />
              <div>
                <div>г. Москва, ул. Пушкина, д. 12</div>
                <div className="mt-1" style={{ color: "#4A6480", fontSize: "12px" }}>
                  м. Чистые пруды, 5 мин пешком
                </div>
                <div className="mt-2" style={{ fontSize: "12px", color: "#4A6480" }}>
                  Пн–Пт: 09:00–20:00<br />Сб–Вс: 09:00–18:00
                </div>
              </div>
            </div>
          </div>
        </div>

        <div
          className="pt-6 flex flex-col md:flex-row items-center justify-between gap-3"
          style={{ borderTop: "1px solid rgba(255,255,255,0.08)" }}
        >
          <p style={{ fontSize: "12px", color: "#4A6480" }}>© 2026 Aster Dental. Все права защищены.</p>
          <div className="flex gap-5">
            {["Политика конфиденциальности", "Условия использования"].map((l) => (
              <a key={l} href="#" style={{ fontSize: "12px", color: "#4A6480" }}>{l}</a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
