import { useState } from "react";
import { Page } from "../App";
import { Header } from "./shared/Header";
import { Footer } from "./shared/Footer";
import {
  ChevronRight,
  Shield,
  Star,
  Clock,
  Smile,
  ArrowRight,
  Check,
} from "lucide-react";
import {
  clinicServices,
  demoClinicBrand,
  serviceAdvantages,
  serviceCategories,
} from "../services/demoClinicContent";

interface Props {
  onNavigate: (page: Page) => void;
}

export function ServicesPage({ onNavigate }: Props) {
  const [activeCategory, setActiveCategory] = useState("all");

  const filtered = activeCategory === "all"
    ? clinicServices
    : clinicServices.filter((s) => s.category === activeCategory);

  const advantageIcons = [Shield, Star, Clock, Smile, Check, Shield];

  return (
    <div style={{ fontFamily: "'Inter', sans-serif", backgroundColor: "#F7F9FC", color: "#1A2B3C" }}>
      <Header onNavigate={onNavigate} activePage="services" />

      {/* Hero */}
      <section
        className="relative"
        style={{ background: "linear-gradient(135deg, #1B6CA8 0%, #0F4C7A 100%)" }}
      >
        <div className="max-w-5xl mx-auto px-5 py-14 md:py-20">
          <div
            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full mb-4"
            style={{ backgroundColor: "rgba(255,255,255,0.12)" }}
          >
            <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: "#4FC3D4" }} />
            <span style={{ color: "#C8E6F5", fontSize: "12px", fontWeight: 500 }}>{demoClinicBrand.name}</span>
          </div>
          <h1
            style={{
              fontSize: "clamp(24px, 4vw, 36px)",
              fontWeight: 700,
              color: "#FFFFFF",
              lineHeight: 1.25,
              marginBottom: "14px",
              maxWidth: "520px",
            }}
          >
            Ортодонтия, эстетика и лечение, где пациенту заранее понятен путь к результату
          </h1>
          <p style={{ color: "#B8D4E8", fontSize: "15px", lineHeight: 1.7, maxWidth: "500px", marginBottom: "24px" }}>
            Lab Smile собран вокруг улыбки как результата: консультация, гигиена, лечение, брекеты, элайнеры, виниры и реставрации в одном спокойном маршруте.
          </p>
          <button
            onClick={() => onNavigate("booking")}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl transition-all"
            style={{ backgroundColor: "#FFFFFF", color: "#1B6CA8", fontSize: "14px", fontWeight: 600 }}
          >
            Записаться на приём
            <ArrowRight size={16} />
          </button>
        </div>
      </section>

      {/* Category Filter */}
      <section className="max-w-5xl mx-auto px-5 py-8">
        <div className="flex gap-2 flex-wrap">
          {serviceCategories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className="px-4 py-2 rounded-xl transition-all"
              style={{
                backgroundColor: activeCategory === cat.id ? "#1B6CA8" : "#FFFFFF",
                color: activeCategory === cat.id ? "#FFFFFF" : "#4A6480",
                border: `1px solid ${activeCategory === cat.id ? "#1B6CA8" : "#E8EEF4"}`,
                fontSize: "13px",
                fontWeight: activeCategory === cat.id ? 600 : 400,
              }}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </section>

      {/* Services Grid */}
      <section className="max-w-5xl mx-auto px-5 pb-12">
        <div className="grid md:grid-cols-2 gap-4">
          {filtered.map((service) => (
            <div
              key={service.id}
              className="rounded-2xl p-5 flex flex-col gap-4 transition-all group"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
            >
              <div className="flex items-start gap-4">
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center shrink-0 text-xl"
                  style={{ backgroundColor: "#EBF4FB" }}
                >
                  {service.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <div style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>{service.name}</div>
                  <div className="flex items-center gap-3 mt-1">
                    <span style={{ fontSize: "13px", fontWeight: 600, color: "#1B6CA8" }}>{service.price}</span>
                    <span style={{ fontSize: "12px", color: "#6B8FA8" }}>· {service.duration}</span>
                  </div>
                </div>
              </div>
              <p style={{ fontSize: "13px", color: "#4A6480", lineHeight: 1.65 }}>{service.desc}</p>
              <div className="flex items-center justify-between">
                <div className="flex gap-1.5 flex-wrap">
                  {service.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-2.5 py-0.5 rounded-full"
                      style={{ backgroundColor: "#F0F5FA", color: "#4A6480", fontSize: "11px" }}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
                <button
                  onClick={() => onNavigate("booking")}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all shrink-0 ml-2"
                  style={{ backgroundColor: "#EBF4FB", color: "#1B6CA8", fontSize: "12px", fontWeight: 500 }}
                >
                  Записаться
                  <ChevronRight size={13} />
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Advantages */}
      <section style={{ backgroundColor: "#FFFFFF", borderTop: "1px solid #E8EEF4", borderBottom: "1px solid #E8EEF4" }}>
        <div className="max-w-5xl mx-auto px-5 py-14">
          <div className="text-center mb-10">
            <h2 style={{ fontWeight: 700, fontSize: "clamp(20px, 3vw, 28px)", color: "#1A2B3C", marginBottom: "8px" }}>
              Почему этот формат клиники удобен пациенту
            </h2>
            <p style={{ fontSize: "14px", color: "#6B8FA8" }}>
              Не просто список услуг, а понятная система лечения и эстетики улыбки
            </p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-5">
            {serviceAdvantages.map((a, i) => {
              const Icon = advantageIcons[i] ?? Shield;

              return (
                <div key={i} className="flex flex-col gap-3">
                  <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center"
                    style={{ backgroundColor: "#EBF4FB", color: "#1B6CA8" }}
                  >
                    <Icon size={20} />
                  </div>
                  <div style={{ fontWeight: 600, fontSize: "14px", color: "#1A2B3C" }}>{a.title}</div>
                  <div style={{ fontSize: "13px", color: "#6B8FA8", lineHeight: 1.6 }}>{a.desc}</div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-5xl mx-auto px-5 py-14">
        <div
          className="rounded-3xl p-8 md:p-12 text-center relative overflow-hidden"
          style={{ background: "linear-gradient(135deg, #1B6CA8 0%, #0F4C7A 100%)" }}
        >
          <div
            className="absolute -right-12 -top-12 w-48 h-48 rounded-full opacity-10"
            style={{ backgroundColor: "#FFFFFF" }}
          />
          <div
            className="absolute -left-8 bottom-0 w-32 h-32 rounded-full opacity-5"
            style={{ backgroundColor: "#FFFFFF" }}
          />
          <div className="relative">
            <h2 style={{ fontWeight: 700, fontSize: "clamp(20px, 3vw, 28px)", color: "#FFFFFF", marginBottom: "12px" }}>
              Хотите собрать понятный план лечения?
            </h2>
            <p style={{ fontSize: "14px", color: "rgba(255,255,255,0.75)", marginBottom: "24px" }}>
              Запишитесь на консультацию и начните с аккуратной диагностики без лишних шагов и скрытых условий
            </p>
            <button
              onClick={() => onNavigate("booking")}
              className="inline-flex items-center gap-2 px-7 py-3.5 rounded-xl transition-all"
              style={{ backgroundColor: "#FFFFFF", color: "#1B6CA8", fontSize: "15px", fontWeight: 600 }}
            >
              Записаться на приём
              <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </section>

      <Footer onNavigate={onNavigate} />
    </div>
  );
}
