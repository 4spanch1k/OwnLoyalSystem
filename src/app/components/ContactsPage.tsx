import { Page } from "../App";
import { Header } from "./shared/Header";
import { Footer } from "./shared/Footer";
import { MapPin, Phone, Mail, MessageCircle, Clock, Instagram, ArrowRight } from "lucide-react";

interface Props {
  onNavigate: (page: Page) => void;
}

export function ContactsPage({ onNavigate }: Props) {
  return (
    <div style={{ fontFamily: "'Inter', sans-serif", backgroundColor: "#F7F9FC", color: "#1A2B3C" }}>
      <Header onNavigate={onNavigate} activePage="contacts" />

      {/* Hero */}
      <section className="max-w-5xl mx-auto px-5 py-12 md:py-16">
        <div className="max-w-2xl">
          <div
            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full mb-4"
            style={{ backgroundColor: "#EBF4FB" }}
          >
            <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: "#1B6CA8" }} />
            <span style={{ color: "#1B6CA8", fontSize: "12px", fontWeight: 500 }}>Мы рядом</span>
          </div>
          <h1
            style={{
              fontSize: "clamp(24px, 4vw, 36px)",
              fontWeight: 700,
              color: "#1A2B3C",
              lineHeight: 1.25,
              marginBottom: "14px",
            }}
          >
            Контакты и адрес клиники
          </h1>
          <p style={{ fontSize: "14px", color: "#4A6480", lineHeight: 1.7 }}>
            Мы находимся в самом центре Москвы, в 5 минутах ходьбы от метро.
          </p>
        </div>
      </section>

      {/* Main grid */}
      <section className="max-w-5xl mx-auto px-5 pb-12">
        <div className="grid md:grid-cols-2 gap-6">
          {/* Map placeholder */}
          <div
            className="rounded-3xl overflow-hidden relative"
            style={{ minHeight: "380px", backgroundColor: "#D6E6F2" }}
          >
            {/* Stylised map placeholder */}
            <div
              className="absolute inset-0 flex flex-col items-center justify-center gap-4"
              style={{
                background: "linear-gradient(135deg, #D6E8F5 0%, #C0D9EE 100%)",
              }}
            >
              {/* Grid lines */}
              <svg className="absolute inset-0 w-full h-full opacity-20" xmlns="http://www.w3.org/2000/svg">
                <defs>
                  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1B6CA8" strokeWidth="0.5"/>
                  </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#grid)" />
              </svg>
              {/* Streets */}
              <div className="absolute inset-0 flex items-center justify-center opacity-30">
                <div className="w-full h-12" style={{ backgroundColor: "#FFFFFF" }} />
              </div>
              <div className="absolute inset-0 flex items-center justify-center opacity-20">
                <div className="h-full w-16" style={{ backgroundColor: "#FFFFFF" }} />
              </div>
              {/* Pin */}
              <div className="relative z-10 flex flex-col items-center gap-3">
                <div
                  className="w-16 h-16 rounded-full flex items-center justify-center shadow-lg"
                  style={{ backgroundColor: "#1B6CA8" }}
                >
                  <MapPin size={28} color="#FFFFFF" />
                </div>
                <div
                  className="px-4 py-2.5 rounded-xl text-center shadow-md"
                  style={{ backgroundColor: "#FFFFFF" }}
                >
                  <div style={{ fontWeight: 700, fontSize: "14px", color: "#1A2B3C" }}>Aster Dental</div>
                  <div style={{ fontSize: "12px", color: "#6B8FA8", marginTop: "2px" }}>
                    ул. Пушкина, д. 12
                  </div>
                </div>
              </div>
              <div
                className="absolute bottom-4 right-4 px-3 py-1.5 rounded-lg"
                style={{ backgroundColor: "rgba(255,255,255,0.9)", fontSize: "11px", color: "#4A6480" }}
              >
                м. Чистые пруды — 5 мин
              </div>
            </div>
          </div>

          {/* Info cards */}
          <div className="flex flex-col gap-4">
            {/* Address */}
            <div
              className="rounded-2xl p-5"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
            >
              <div className="flex items-center gap-3 mb-4">
                <div
                  className="w-9 h-9 rounded-xl flex items-center justify-center"
                  style={{ backgroundColor: "#EBF4FB" }}
                >
                  <MapPin size={16} style={{ color: "#1B6CA8" }} />
                </div>
                <span style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>Адрес</span>
              </div>
              <p style={{ fontSize: "14px", color: "#1A2B3C", fontWeight: 500, marginBottom: "6px" }}>
                г. Москва, ул. Пушкина, д. 12, стр. 1
              </p>
              <p style={{ fontSize: "13px", color: "#6B8FA8", lineHeight: 1.6 }}>
                м. Чистые пруды (Сокольническая линия), 5 минут пешком. Выход № 2, затем по ул. Пушкина направо.
              </p>
            </div>

            {/* Phone */}
            <div
              className="rounded-2xl p-5"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ backgroundColor: "#EBF4FB" }}>
                  <Phone size={16} style={{ color: "#1B6CA8" }} />
                </div>
                <span style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>Телефон</span>
              </div>
              <a href="tel:+78001234567" style={{ fontSize: "20px", fontWeight: 700, color: "#1B6CA8" }}>
                +7 (800) 123-45-67
              </a>
              <p style={{ fontSize: "12px", color: "#6B8FA8", marginTop: "4px" }}>Бесплатный звонок по России</p>
              <div className="flex gap-2 mt-4">
                <a
                  href="https://wa.me/78001234567"
                  className="flex items-center gap-2 px-4 py-2 rounded-xl transition-all"
                  style={{ backgroundColor: "#E8F5E9", color: "#1B7A3E", fontSize: "13px", fontWeight: 500 }}
                >
                  <MessageCircle size={14} />
                  WhatsApp
                </a>
                <a
                  href="https://instagram.com"
                  className="flex items-center gap-2 px-4 py-2 rounded-xl transition-all"
                  style={{ backgroundColor: "#FFF0F8", color: "#C2185B", fontSize: "13px", fontWeight: 500 }}
                >
                  <Instagram size={14} />
                  Instagram
                </a>
              </div>
            </div>

            {/* Email */}
            <div
              className="rounded-2xl p-5"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ backgroundColor: "#EBF4FB" }}>
                  <Mail size={16} style={{ color: "#1B6CA8" }} />
                </div>
                <span style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>Email</span>
              </div>
              <a href="mailto:info@asterdental.ru" style={{ fontSize: "15px", fontWeight: 600, color: "#1B6CA8" }}>
                info@asterdental.ru
              </a>
              <p style={{ fontSize: "12px", color: "#6B8FA8", marginTop: "4px" }}>Ответим в течение 2 часов</p>
            </div>

            {/* Schedule */}
            <div
              className="rounded-2xl p-5"
              style={{ backgroundColor: "#EBF4FB", border: "1px solid #D0E6F5" }}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ backgroundColor: "#FFFFFF" }}>
                  <Clock size={16} style={{ color: "#1B6CA8" }} />
                </div>
                <span style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>График работы</span>
              </div>
              <div className="flex flex-col gap-2.5">
                {[
                  { days: "Понедельник — Пятница", hours: "09:00 — 20:00" },
                  { days: "Суббота", hours: "09:00 — 18:00" },
                  { days: "Воскресенье", hours: "10:00 — 16:00" },
                ].map((s, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <span style={{ fontSize: "13px", color: "#4A6480" }}>{s.days}</span>
                    <span style={{ fontSize: "13px", fontWeight: 600, color: "#1A2B3C" }}>{s.hours}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section style={{ backgroundColor: "#FFFFFF", borderTop: "1px solid #E8EEF4" }}>
        <div className="max-w-5xl mx-auto px-5 py-14">
          <div
            className="rounded-3xl p-8 md:p-10 flex flex-col md:flex-row items-center justify-between gap-6"
            style={{ background: "linear-gradient(135deg, #1B6CA8 0%, #0F4C7A 100%)" }}
          >
            <div>
              <h2 style={{ fontWeight: 700, fontSize: "22px", color: "#FFFFFF", marginBottom: "8px" }}>
                Хотите записаться к нам?
              </h2>
              <p style={{ fontSize: "14px", color: "rgba(255,255,255,0.7)" }}>
                Первичная консультация — бесплатно. Без очередей, удобное время.
              </p>
            </div>
            <button
              onClick={() => onNavigate("booking")}
              className="shrink-0 flex items-center gap-2 px-6 py-3.5 rounded-xl transition-all"
              style={{ backgroundColor: "#FFFFFF", color: "#1B6CA8", fontSize: "14px", fontWeight: 600 }}
            >
              Записаться онлайн
              <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </section>

      <Footer onNavigate={onNavigate} />
    </div>
  );
}
