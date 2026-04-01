import { Page } from "../App";
import { Header } from "./shared/Header";
import { Footer } from "./shared/Footer";
import { ArrowRight, Star, Award, Clock } from "lucide-react";

interface Props {
  onNavigate: (page: Page) => void;
}

const DOCTORS = [
  {
    id: 1,
    name: "Марина Соколова",
    role: "Терапевт, Пародонтолог",
    experience: "12 лет",
    rating: 4.9,
    reviews: 134,
    photo: "https://images.unsplash.com/photo-1734002886107-168181bcd6a1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmZW1hbGUlMjBkb2N0b3IlMjBzbWlsaW5nJTIwbWVkaWNhbCUyMHByb2Zlc3Npb25hbHxlbnwxfHx8fDE3NzQ5NTYzNzV8MA&ixlib=rb-4.1.0&q=80&w=400",
    desc: "Специализируется на лечении кариеса и заболеваний дёсен. Работает под микроскопом. Мягкий подход, особенно с тревожными пациентами.",
    education: "МГМСУ им. Евдокимова, 2011",
    specialties: ["Кариес", "Пародонтология", "Эндодонтия"],
  },
  {
    id: 2,
    name: "Дмитрий Волков",
    role: "Ортодонт",
    experience: "9 лет",
    rating: 4.8,
    reviews: 89,
    photo: "https://images.unsplash.com/photo-1631596577204-53ad0d6e6978?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtYWxlJTIwb3J0aG9kb250aXN0JTIwZGVudGFsJTIwc3VyZ2VvbiUyMHBvcnRyYWl0fGVufDF8fHx8MTc3NDk1NjM3NXww&ixlib=rb-4.1.0&q=80&w=400",
    desc: "Эксперт по исправлению прикуса у детей и взрослых. Работает с брекетами и элайнерами. Индивидуальный план для каждого пациента.",
    education: "Первый МГМУ им. Сеченова, 2014",
    specialties: ["Брекеты", "Элайнеры", "Прикус детей"],
  },
  {
    id: 3,
    name: "Елена Кравцова",
    role: "Гигиенист, Терапевт",
    experience: "7 лет",
    rating: 5.0,
    reviews: 67,
    photo: "https://images.unsplash.com/photo-1753487050317-919a2b26a6ed?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3b21hbiUyMGh5Z2llbmlzdCUyMGRlbnRhbCUyMGNsaW5pYyUyMHdoaXRlJTIwdW5pZm9ybXxlbnwxfHx8fDE3NzQ5NTYzODl8MA&ixlib=rb-4.1.0&q=80&w=400",
    desc: "Мастер профессиональной гигиены полости рта. Painless-техника чистки и фторирования. Рекомендует эффективный домашний уход.",
    education: "РУДН, Медицинский институт, 2016",
    specialties: ["Профчистка", "Air Flow", "Фторирование"],
  },
  {
    id: 4,
    name: "Игорь Петров",
    role: "Хирург, Имплантолог",
    experience: "15 лет",
    rating: 4.9,
    reviews: 211,
    photo: "https://images.unsplash.com/photo-1588776814546-daab30f310ce?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkZW50aXN0JTIwZG9jdG9yJTIwcHJvZmVzc2lvbmFsJTIwcG9ydHJhaXQlMjB3aGl0ZSUyMGNvYXR8ZW58MXx8fHwxNzc0OTU2MzcwfDA&ixlib=rb-4.1.0&q=80&w=400",
    desc: "Ведущий имплантолог клиники. Более 1 000 успешных имплантаций. Работает с системами Nobel, Straumann. Пожизненная гарантия на имплант.",
    education: "МГМСУ им. Евдокимова, 2009",
    specialties: ["Имплантация", "Хирургия", "Костная пластика"],
  },
];

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
            Врачи, которым доверяют
          </h1>
          <p style={{ fontSize: "14px", color: "#4A6480", lineHeight: 1.7 }}>
            Все специалисты клиники имеют действующие сертификаты, регулярно проходят повышение квалификации и работают на современном оборудовании.
          </p>
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-3 gap-4 mt-8 max-w-lg">
          {[
            { value: "4", label: "специалиста" },
            { value: "43", label: "года опыта суммарно" },
            { value: "1 200+", label: "довольных пациентов" },
          ].map((s, i) => (
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
          {DOCTORS.map((doc) => (
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
            Запишитесь на первичный осмотр — мы сами направим вас к нужному специалисту бесплатно
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
