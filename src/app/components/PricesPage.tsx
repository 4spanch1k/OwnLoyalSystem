import { useState } from "react";
import { Page } from "../App";
import { Header } from "./shared/Header";
import { Footer } from "./shared/Footer";
import { ArrowRight, Info, ChevronDown, ChevronUp } from "lucide-react";
import { priceCategories } from "../services/demoClinicContent";

interface Props {
  onNavigate: (page: Page) => void;
}

export function PricesPage({ onNavigate }: Props) {
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({
    diagnostics: true,
    hygiene: false,
    treatment: false,
    ortho: false,
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
            Мы показываем понятные диапазоны до визита, а точную сумму фиксируем после консультации и плана лечения. Это помогает спокойно обсуждать ортодонтию, виниры, гигиену и терапию без неприятных сюрпризов.
          </p>
        </div>

        {/* Info banner */}
        <div
          className="mt-6 rounded-2xl p-4 flex items-start gap-3"
          style={{ backgroundColor: "#EBF4FB", border: "1px solid #D0E6F5" }}
        >
          <Info size={16} style={{ color: "#1B6CA8", marginTop: "2px", flexShrink: 0 }} />
          <div style={{ fontSize: "13px", color: "#1A2B3C", lineHeight: 1.6 }}>
            <strong>Точная стоимость определяется после консультации.</strong> До визита вы видите понятный ориентир, а на приеме получаете уже конкретный план лечения без скрытых доплат.
          </div>
        </div>
      </section>

      {/* Price accordion */}
      <section className="max-w-5xl mx-auto px-5 pb-12">
        <div className="flex flex-col gap-3">
          {priceCategories.map((cat) => (
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
              Хотите понять бюджет лечения заранее?
            </h2>
            <p style={{ fontSize: "14px", color: "rgba(255,255,255,0.7)" }}>
              Запишитесь на консультацию, чтобы получить понятный план и диапазон стоимости под ваш кейс
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
