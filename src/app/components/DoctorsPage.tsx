import { Page } from "../App";
import { Header } from "./shared/Header";
import { Footer } from "./shared/Footer";
import { ArrowRight, Star, Award, Clock } from "lucide-react";
import { clinicDoctors, doctorStats } from "../services/demoClinicContent";

interface Props {
  onNavigate: (page: Page) => void;
}

export function DoctorsPage({ onNavigate }: Props) {
  return (
    <div style={{ fontFamily: "'Inter', sans-serif", backgroundColor: "#F7F9FC", color: "#1A2B3C" }}>
      <Header onNavigate={onNavigate} activePage="doctors" />

      {/* Hero */}
      <section className="max-w-5xl mx-auto px-5 py-12 md:py-16">
        <div className="max-w-2xl">
          <div
            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full mb-4"
            style={{ backgroundColor: "#EBF4FB" }}
          >
            <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: "#1B6CA8" }} />
            <span style={{ color: "#1B6CA8", fontSize: "12px", fontWeight: 500 }}>Наша команда</span>
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
            Команда, которая ведет пациента от идеи красивой улыбки до аккуратного результата
          </h1>
          <p style={{ fontSize: "14px", color: "#4A6480", lineHeight: 1.7 }}>
            В Lab Smile акцент сделан на ортодонтию, эстетическую терапию, smile design и профилактику, чтобы у пациента был цельный маршрут лечения.
          </p>
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-3 gap-4 mt-8 max-w-lg">
          {doctorStats.map((s, i) => (
            <div key={i} className="rounded-2xl p-4 text-center" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
              <div style={{ fontSize: "22px", fontWeight: 700, color: "#1B6CA8" }}>{s.value}</div>
              <div style={{ fontSize: "11px", color: "#6B8FA8", marginTop: "3px" }}>{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Doctors grid */}
      <section className="max-w-5xl mx-auto px-5 pb-14">
        <div className="grid md:grid-cols-2 gap-5">
          {clinicDoctors.map((doc) => (
            <div
              key={doc.id}
              className="rounded-3xl overflow-hidden"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
            >
              {/* Top photo block */}
              <div className="relative h-52 overflow-hidden" style={{ backgroundColor: "#EBF4FB" }}>
                <img
                  src={doc.photo}
                  alt={doc.name}
                  className="w-full h-full object-cover object-top"
                />
                <div
                  className="absolute inset-0"
                  style={{ background: "linear-gradient(to top, rgba(26,43,60,0.55) 0%, transparent 50%)" }}
                />
                {/* Experience badge */}
                <div
                  className="absolute top-4 right-4 px-3 py-1.5 rounded-full flex items-center gap-1.5"
                  style={{ backgroundColor: "rgba(255,255,255,0.92)", backdropFilter: "blur(8px)" }}
                >
                  <Clock size={12} style={{ color: "#1B6CA8" }} />
                  <span style={{ fontSize: "12px", fontWeight: 600, color: "#1A2B3C" }}>{doc.experience}</span>
                </div>
                {/* Name overlay */}
                <div className="absolute bottom-4 left-4">
                  <div style={{ fontWeight: 700, fontSize: "17px", color: "#FFFFFF" }}>{doc.name}</div>
                  <div style={{ fontSize: "13px", color: "rgba(255,255,255,0.8)" }}>{doc.role}</div>
                </div>
              </div>

              {/* Content */}
              <div className="p-5">
                {/* Rating */}
                <div className="flex items-center gap-3 mb-4">
                  <div className="flex items-center gap-1.5">
                    <Star size={14} style={{ color: "#FFB800" }} fill="#FFB800" />
                    <span style={{ fontSize: "14px", fontWeight: 600, color: "#1A2B3C" }}>{doc.rating}</span>
                  </div>
                  <span style={{ fontSize: "12px", color: "#6B8FA8" }}>{doc.reviews} отзывов</span>
                  <div className="flex items-center gap-1.5 ml-auto">
                    <Award size={13} style={{ color: "#1B6CA8" }} />
                    <span style={{ fontSize: "12px", color: "#4A6480" }}>Сертифицирован</span>
                  </div>
                </div>

                <p style={{ fontSize: "13px", color: "#4A6480", lineHeight: 1.65, marginBottom: "14px" }}>
                  {doc.desc}
                </p>

                {/* Education */}
                <div
                  className="px-3 py-2.5 rounded-xl mb-4"
                  style={{ backgroundColor: "#F7F9FC", fontSize: "12px", color: "#6B8FA8" }}
                >
                  🎓 {doc.education}
                </div>

                {/* Specialties */}
                <div className="flex gap-1.5 flex-wrap mb-5">
                  {doc.specialties.map((sp) => (
                    <span
                      key={sp}
                      className="px-2.5 py-1 rounded-lg"
                      style={{ backgroundColor: "#EBF4FB", color: "#1B6CA8", fontSize: "11px", fontWeight: 500 }}
                    >
                      {sp}
                    </span>
                  ))}
                </div>

                <button
                  onClick={() => onNavigate("booking")}
                  className="w-full py-3 rounded-xl flex items-center justify-center gap-2 transition-all"
                  style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}
                >
                  Записаться к врачу
                  <ArrowRight size={15} />
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section style={{ backgroundColor: "#FFFFFF", borderTop: "1px solid #E8EEF4" }}>
        <div className="max-w-5xl mx-auto px-5 py-14 text-center">
          <h2 style={{ fontWeight: 700, fontSize: "22px", color: "#1A2B3C", marginBottom: "10px" }}>
            Не знаете, к кому записаться?
          </h2>
            <p style={{ fontSize: "14px", color: "#6B8FA8", marginBottom: "24px" }}>
            Если не уверены, с чего начать, приходите на первичную консультацию — подберем понятный следующий шаг без лишней сложности
          </p>
          <button
            onClick={() => onNavigate("booking")}
            className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl transition-all"
            style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}
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
