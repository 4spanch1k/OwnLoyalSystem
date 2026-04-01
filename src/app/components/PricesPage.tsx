import { useState } from "react";
import { Page } from "../App";
import { Header } from "./shared/Header";
import { Footer } from "./shared/Footer";
import { ArrowRight, Info, ChevronDown, ChevronUp } from "lucide-react";

interface Props {
  onNavigate: (page: Page) => void;
}

const PRICE_CATEGORIES = [
  {
    id: "prevention",
    label: "Профилактика",
    icon: "🦷",
    items: [
      { name: "Первичная консультация", price: "Бесплатно", note: "" },
      { name: "Профессиональная чистка (ультразвук + Air Flow)", price: "3 000 – 5 000 ₽", note: "" },
      { name: "Фторирование зубов", price: "1 200 – 2 000 ₽", note: "" },
      { name: "Чистка зубного камня (1 зуб)", price: "300 – 500 ₽", note: "" },
      { name: "Ортопантомограмма (панорамный снимок)", price: "900 – 1 200 ₽", note: "" },
    ],
  },
  {
    id: "treatment",
    label: "Лечение",
    icon: "🔬",
    items: [
      { name: "Лечение кариеса (световая пломба)", price: "4 500 – 8 000 ₽", note: "зависит от сложности" },
      { name: "Лечение пульпита (1 канал)", price: "8 000 – 12 000 ₽", note: "" },
      { name: "Лечение пульпита (3 канала)", price: "14 000 – 20 000 ₽", note: "" },
      { name: "Удаление простого зуба", price: "2 500 – 4 000 ₽", note: "" },
      { name: "Удаление сложного зуба (хирургия)", price: "5 000 – 9 000 ₽", note: "" },
      { name: "Лечение под микроскопом", price: "от 12 000 ₽", note: "за зуб" },
    ],
  },
  {
    id: "ortho",
    label: "Ортодонтия",
    icon: "😁",
    items: [
      { name: "Консультация ортодонта", price: "Бесплатно", note: "" },
      { name: "Металлические брекеты (полная система)", price: "55 000 – 75 000 ₽", note: "" },
      { name: "Керамические брекеты (полная система)", price: "75 000 – 95 000 ₽", note: "" },
      { name: "Сапфировые брекеты (полная система)", price: "95 000 – 120 000 ₽", note: "" },
      { name: "Элайнеры (1 курс)", price: "от 80 000 ₽", note: "" },
      { name: "Ретейнеры (после брекетов)", price: "5 000 – 8 000 ₽", note: "за одну челюсть" },
    ],
  },
  {
    id: "implant",
    label: "Имплантация и протезирование",
    icon: "🔩",
    items: [
      { name: "Имплант (под ключ)", price: "от 45 000 ₽", note: "включая коронку" },
      { name: "Коронка металлокерамическая", price: "12 000 – 16 000 ₽", note: "" },
      { name: "Коронка циркониевая", price: "18 000 – 28 000 ₽", note: "" },
      { name: "Коронка E-max (безметалловая)", price: "22 000 – 32 000 ₽", note: "" },
      { name: "Съёмный протез (акриловый)", price: "от 22 000 ₽", note: "" },
    ],
  },
  {
    id: "aesthetics",
    label: "Эстетическая стоматология",
    icon: "✨",
    items: [
      { name: "Отбеливание Zoom 4 (полный курс)", price: "12 000 – 18 000 ₽", note: "" },
      { name: "Домашнее отбеливание (каппы + гель)", price: "5 000 – 8 000 ₽", note: "" },
      { name: "Винир керамический (1 зуб)", price: "22 000 – 32 000 ₽", note: "" },
      { name: "Скайс / украшение на зуб", price: "2 500 – 4 000 ₽", note: "" },
    ],
  },
];

export function PricesPage({ onNavigate }: Props) {
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({
    prevention: true,
    treatment: false,
    ortho: false,
    implant: false,
    aesthetics: false,
  });

  const toggle = (id: string) => {
    setOpenSections((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div style={{ fontFamily: "'Inter', sans-serif", backgroundColor: "#F7F9FC", color: "#1A2B3C" }}>
      <Header onNavigate={onNavigate} activePage="prices" />

      {/* Hero */}
      <section className="max-w-5xl mx-auto px-5 py-12 md:py-16">
        <div className="max-w-2xl">
          <div
            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full mb-4"
            style={{ backgroundColor: "#EBF4FB" }}
          >
            <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: "#1B6CA8" }} />
            <span style={{ color: "#1B6CA8", fontSize: "12px", fontWeight: 500 }}>Прозрачные цены</span>
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
            Стоимость услуг клиники
          </h1>
          <p style={{ fontSize: "14px", color: "#4A6480", lineHeight: 1.7 }}>
            Цены носят ознакомительный характер. Точная стоимость определяется на консультации после осмотра — это зависит от индивидуальной клинической картины. Первичный осмотр и консультация — бесплатно.
          </p>
        </div>

        {/* Info banner */}
        <div
          className="mt-6 rounded-2xl p-4 flex items-start gap-3"
          style={{ backgroundColor: "#EBF4FB", border: "1px solid #D0E6F5" }}
        >
          <Info size={16} style={{ color: "#1B6CA8", marginTop: "2px", flexShrink: 0 }} />
          <div style={{ fontSize: "13px", color: "#1A2B3C", lineHeight: 1.6 }}>
            <strong>Первичная консультация — бесплатно.</strong> Запишитесь к врачу, пройдите осмотр и получите точный план лечения с ценами. Мы не навязываем лишнего.
          </div>
        </div>
      </section>

      {/* Price accordion */}
      <section className="max-w-5xl mx-auto px-5 pb-12">
        <div className="flex flex-col gap-3">
          {PRICE_CATEGORIES.map((cat) => (
            <div
              key={cat.id}
              className="rounded-2xl overflow-hidden"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
            >
              {/* Category header */}
              <button
                onClick={() => toggle(cat.id)}
                className="w-full flex items-center justify-between px-5 py-4 transition-all"
                style={{ backgroundColor: openSections[cat.id] ? "#F7F9FC" : "#FFFFFF" }}
              >
                <div className="flex items-center gap-3">
                  <span className="text-xl">{cat.icon}</span>
                  <span style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>{cat.label}</span>
                  <span
                    className="px-2 py-0.5 rounded-full"
                    style={{ backgroundColor: "#EBF4FB", color: "#1B6CA8", fontSize: "11px", fontWeight: 500 }}
                  >
                    {cat.items.length} услуг
                  </span>
                </div>
                {openSections[cat.id]
                  ? <ChevronUp size={18} style={{ color: "#6B8FA8" }} />
                  : <ChevronDown size={18} style={{ color: "#6B8FA8" }} />
                }
              </button>

              {/* Items */}
              {openSections[cat.id] && (
                <div style={{ borderTop: "1px solid #E8EEF4" }}>
                  {cat.items.map((item, idx) => (
                    <div
                      key={idx}
                      className="flex items-center justify-between px-5 py-3.5"
                      style={{
                        borderBottom: idx < cat.items.length - 1 ? "1px solid #F0F5FA" : "none",
                      }}
                    >
                      <div>
                        <div style={{ fontSize: "14px", color: "#1A2B3C" }}>{item.name}</div>
                        {item.note && (
                          <div style={{ fontSize: "11px", color: "#6B8FA8", marginTop: "2px" }}>{item.note}</div>
                        )}
                      </div>
                      <div
                        className="shrink-0 ml-4 px-3 py-1.5 rounded-lg"
                        style={{ backgroundColor: "#F0F5FA", color: "#1B6CA8", fontSize: "13px", fontWeight: 600 }}
                      >
                        {item.price}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-5xl mx-auto px-5 pb-14">
        <div
          className="rounded-3xl p-8 md:p-10 flex flex-col md:flex-row items-center justify-between gap-6"
          style={{ background: "linear-gradient(135deg, #1B6CA8 0%, #0F4C7A 100%)" }}
        >
          <div>
            <h2 style={{ fontWeight: 700, fontSize: "22px", color: "#FFFFFF", marginBottom: "8px" }}>
              Точная стоимость — после консультации
            </h2>
            <p style={{ fontSize: "14px", color: "rgba(255,255,255,0.7)" }}>
              Запишитесь на бесплатный осмотр — врач составит план лечения и озвучит итоговую цену
            </p>
          </div>
          <button
            onClick={() => onNavigate("booking")}
            className="shrink-0 flex items-center gap-2 px-6 py-3.5 rounded-xl transition-all"
            style={{ backgroundColor: "#FFFFFF", color: "#1B6CA8", fontSize: "14px", fontWeight: 600 }}
          >
            Записаться на консультацию
            <ArrowRight size={16} />
          </button>
        </div>
      </section>

      <Footer onNavigate={onNavigate} />
    </div>
  );
}
