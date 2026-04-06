import { useState } from "react";
import { Page } from "../App";
import { Header } from "./shared/Header";
import { Footer } from "./shared/Footer";
import { Check, ChevronRight, ChevronLeft, Calendar, Clock, User, Phone, Mail } from "lucide-react";
import { bookingDoctors, bookingServices, demoClinicBrand } from "../services/demoClinicContent";

interface Props {
  onNavigate: (page: Page) => void;
}

type Step = 1 | 2 | 3 | 4;

const DATES = [
  { date: "7 апр", day: "Пн", slots: 5 },
  { date: "8 апр", day: "Вт", slots: 3 },
  { date: "9 апр", day: "Ср", slots: 0 },
  { date: "10 апр", day: "Чт", slots: 7 },
  { date: "11 апр", day: "Пт", slots: 4 },
  { date: "12 апр", day: "Сб", slots: 2 },
  { date: "14 апр", day: "Пн", slots: 6 },
];

const TIMES_AM = ["09:00", "10:00", "11:00"];
const TIMES_PM = ["13:00", "14:30", "16:00", "17:30", "19:00"];

const STEP_LABELS = ["Услуга", "Врач", "Время", "Данные"];

export function BookingPage({ onNavigate }: Props) {
  const [step, setStep] = useState<Step>(1);
  const [selected, setSelected] = useState({
    service: "",
    doctor: "",
    date: "",
    time: "",
    name: "",
    phone: "",
    email: "",
    comment: "",
  });

  const update = (key: string, val: string) => setSelected((p) => ({ ...p, [key]: val }));

  const canProceed = () => {
    if (step === 1) return !!selected.service;
    if (step === 2) return !!selected.doctor;
    if (step === 3) return !!selected.date && !!selected.time;
    if (step === 4) return !!selected.name && !!selected.phone;
    return false;
  };

  const next = () => { if (canProceed()) setStep((s) => (s + 1) as Step); };
  const prev = () => setStep((s) => (s - 1) as Step);

  if (step === 5 as unknown as Step) {
    return (
      <div style={{ fontFamily: "'Inter', sans-serif", backgroundColor: "#F7F9FC" }}>
        <Header onNavigate={onNavigate} />
        <div className="min-h-[70vh] flex items-center justify-center px-5 py-16">
          <div
            className="rounded-3xl p-10 text-center max-w-md w-full"
            style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
          >
            <div
              className="w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6"
              style={{ backgroundColor: "#E6F5ED" }}
            >
              <Check size={36} color="#22A05B" />
            </div>
            <h1 style={{ fontWeight: 700, fontSize: "24px", color: "#1A2B3C", marginBottom: "12px" }}>
              Запись подтверждена!
            </h1>
            <p style={{ fontSize: "14px", color: "#6B8FA8", lineHeight: 1.7, marginBottom: "8px" }}>
              Ваша запись принята. Мы отправили подтверждение на указанный номер телефона.
            </p>
            <div
              className="rounded-2xl p-4 my-6 text-left"
              style={{ backgroundColor: "#F7F9FC" }}
            >
              {[
                { label: "Услуга", value: bookingServices.find((s) => s.id === selected.service)?.name },
                { label: "Врач", value: bookingDoctors.find((d) => String(d.id) === selected.doctor)?.name },
                { label: "Дата", value: `${selected.date}, ${selected.time}` },
                { label: "Пациент", value: selected.name },
              ].map((r) => (
                <div key={r.label} className="flex items-start justify-between py-2" style={{ borderBottom: "1px solid #E8EEF4" }}>
                  <span style={{ fontSize: "12px", color: "#6B8FA8" }}>{r.label}</span>
                  <span style={{ fontSize: "13px", fontWeight: 500, color: "#1A2B3C" }}>{r.value}</span>
                </div>
              ))}
            </div>
            <div className="flex flex-col gap-3">
              <button
                onClick={() => onNavigate("cabinet")}
                className="w-full py-3 rounded-xl"
                style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}
              >
                Перейти в личный кабинет
              </button>
              <button
                onClick={() => onNavigate("public")}
                className="w-full py-3 rounded-xl"
                style={{ backgroundColor: "#F7F9FC", color: "#4A6480", fontSize: "14px", fontWeight: 500, border: "1px solid #E8EEF4" }}
              >
                На главную
              </button>
            </div>
          </div>
        </div>
        <Footer onNavigate={onNavigate} />
      </div>
    );
  }

  return (
    <div style={{ fontFamily: "'Inter', sans-serif", backgroundColor: "#F7F9FC", color: "#1A2B3C" }}>
      <Header onNavigate={onNavigate} />

      <section className="max-w-3xl mx-auto px-5 py-10">
        {/* Page title */}
        <div className="mb-8">
          <h1 style={{ fontWeight: 700, fontSize: "clamp(22px, 4vw, 30px)", color: "#1A2B3C", marginBottom: "6px" }}>
            Запись на приём
          </h1>
          <p style={{ fontSize: "13px", color: "#6B8FA8" }}>
            Оставьте заявку, и {demoClinicBrand.name} подтвердит запись в рабочее время
          </p>
        </div>

        {/* Progress steps */}
        <div className="flex items-center gap-0 mb-8">
          {STEP_LABELS.map((label, i) => {
            const n = i + 1;
            const done = step > n;
            const active = step === n;
            return (
              <div key={label} className="flex items-center flex-1">
                <div className="flex flex-col items-center flex-1">
                  <div
                    className="w-8 h-8 rounded-full flex items-center justify-center transition-all"
                    style={{
                      backgroundColor: done ? "#22A05B" : active ? "#1B6CA8" : "#E8EEF4",
                      color: done || active ? "#FFFFFF" : "#6B8FA8",
                      fontSize: "13px",
                      fontWeight: 600,
                    }}
                  >
                    {done ? <Check size={14} /> : n}
                  </div>
                  <div
                    style={{
                      fontSize: "11px",
                      marginTop: "5px",
                      color: active ? "#1B6CA8" : done ? "#22A05B" : "#6B8FA8",
                      fontWeight: active ? 600 : 400,
                    }}
                  >
                    {label}
                  </div>
                </div>
                {i < STEP_LABELS.length - 1 && (
                  <div
                    className="flex-1 h-px mx-1"
                    style={{ backgroundColor: step > n ? "#22A05B" : "#E8EEF4", marginBottom: "20px" }}
                  />
                )}
              </div>
            );
          })}
        </div>

        {/* Step 1 — Service */}
        {step === 1 && (
          <div
            className="rounded-2xl p-6"
            style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
          >
            <h2 style={{ fontWeight: 600, fontSize: "17px", color: "#1A2B3C", marginBottom: "4px" }}>
              Выберите услугу
            </h2>
            <p style={{ fontSize: "13px", color: "#6B8FA8", marginBottom: "20px" }}>
              Если не уверены в формате лечения, начните с первичной консультации
            </p>
            <div className="grid sm:grid-cols-2 gap-3">
              {bookingServices.map((s) => (
                <button
                  key={s.id}
                  onClick={() => update("service", s.id)}
                  className="p-4 rounded-xl text-left flex items-start gap-3 transition-all"
                  style={{
                    backgroundColor: selected.service === s.id ? "#EBF4FB" : "#F7F9FC",
                    border: `1px solid ${selected.service === s.id ? "#1B6CA8" : "#E8EEF4"}`,
                  }}
                >
                  <span className="text-2xl">{s.icon}</span>
                  <div className="flex-1 min-w-0">
                    <div style={{ fontWeight: 500, fontSize: "14px", color: "#1A2B3C" }}>{s.name}</div>
                    <div className="flex items-center gap-2 mt-1">
                      <span style={{ fontSize: "12px", fontWeight: 600, color: "#1B6CA8" }}>{s.price}</span>
                      <span style={{ fontSize: "11px", color: "#6B8FA8" }}>· {s.duration}</span>
                    </div>
                  </div>
                  {selected.service === s.id && (
                    <Check size={15} style={{ color: "#1B6CA8", flexShrink: 0, marginTop: "2px" }} />
                  )}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Step 2 — Doctor */}
        {step === 2 && (
          <div
            className="rounded-2xl p-6"
            style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
          >
            <h2 style={{ fontWeight: 600, fontSize: "17px", color: "#1A2B3C", marginBottom: "4px" }}>
              Выберите врача
            </h2>
            <p style={{ fontSize: "13px", color: "#6B8FA8", marginBottom: "20px" }}>
              Или оставьте выбор клинике — мы подберём специалиста
            </p>
            <div className="flex flex-col gap-3">
              <button
                onClick={() => update("doctor", "any")}
                className="p-4 rounded-xl text-left flex items-center gap-3 transition-all"
                style={{
                  backgroundColor: selected.doctor === "any" ? "#EBF4FB" : "#F7F9FC",
                  border: `1px solid ${selected.doctor === "any" ? "#1B6CA8" : "#E8EEF4"}`,
                }}
              >
                <div
                  className="w-10 h-10 rounded-xl flex items-center justify-center"
                  style={{ backgroundColor: "#EBF4FB" }}
                >
                  <User size={18} style={{ color: "#1B6CA8" }} />
                </div>
                <div>
                  <div style={{ fontWeight: 600, fontSize: "14px", color: "#1A2B3C" }}>Любой доступный врач</div>
                  <div style={{ fontSize: "12px", color: "#6B8FA8" }}>Ближайшее свободное время</div>
                </div>
                {selected.doctor === "any" && <Check size={15} style={{ color: "#1B6CA8", marginLeft: "auto" }} />}
              </button>
              {bookingDoctors.map((doc) => (
                <button
                  key={doc.id}
                  onClick={() => update("doctor", String(doc.id))}
                  className="p-4 rounded-xl text-left flex items-center gap-3 transition-all"
                  style={{
                    backgroundColor: selected.doctor === String(doc.id) ? "#EBF4FB" : "#F7F9FC",
                    border: `1px solid ${selected.doctor === String(doc.id) ? "#1B6CA8" : "#E8EEF4"}`,
                  }}
                >
                  <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
                    style={{ backgroundColor: "#1B6CA8" }}
                  >
                    <span style={{ color: "#fff", fontWeight: 700, fontSize: "15px" }}>
                      {doc.name.charAt(0)}
                    </span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div style={{ fontWeight: 600, fontSize: "14px", color: "#1A2B3C" }}>{doc.name}</div>
                    <div style={{ fontSize: "12px", color: "#6B8FA8" }}>{doc.role}</div>
                  </div>
                  {selected.doctor === String(doc.id) && <Check size={15} style={{ color: "#1B6CA8", flexShrink: 0 }} />}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Step 3 — Date & Time */}
        {step === 3 && (
          <div className="flex flex-col gap-4">
            <div
              className="rounded-2xl p-6"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
            >
              <div className="flex items-center gap-2 mb-4">
                <Calendar size={16} style={{ color: "#1B6CA8" }} />
                <h2 style={{ fontWeight: 600, fontSize: "16px", color: "#1A2B3C" }}>Выберите дату</h2>
              </div>
              <div className="grid grid-cols-4 sm:grid-cols-7 gap-2">
                {DATES.map((d) => (
                  <button
                    key={d.date}
                    onClick={() => d.slots > 0 && update("date", d.date)}
                    disabled={d.slots === 0}
                    className="flex flex-col items-center py-3 px-2 rounded-xl transition-all"
                    style={{
                      backgroundColor: selected.date === d.date ? "#1B6CA8" : d.slots === 0 ? "#F0F5FA" : "#F7F9FC",
                      border: `1px solid ${selected.date === d.date ? "#1B6CA8" : "#E8EEF4"}`,
                      opacity: d.slots === 0 ? 0.5 : 1,
                      cursor: d.slots === 0 ? "not-allowed" : "pointer",
                    }}
                  >
                    <span style={{ fontSize: "11px", color: selected.date === d.date ? "rgba(255,255,255,0.7)" : "#6B8FA8" }}>
                      {d.day}
                    </span>
                    <span style={{ fontSize: "14px", fontWeight: 600, color: selected.date === d.date ? "#FFFFFF" : "#1A2B3C", marginTop: "2px" }}>
                      {d.date.split(" ")[0]}
                    </span>
                    <span style={{ fontSize: "10px", color: selected.date === d.date ? "rgba(255,255,255,0.6)" : d.slots === 0 ? "#BBCCD8" : "#6B8FA8", marginTop: "2px" }}>
                      {d.slots === 0 ? "занято" : `${d.slots} мест`}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            {selected.date && (
              <div
                className="rounded-2xl p-6"
                style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
              >
                <div className="flex items-center gap-2 mb-4">
                  <Clock size={16} style={{ color: "#1B6CA8" }} />
                  <h2 style={{ fontWeight: 600, fontSize: "16px", color: "#1A2B3C" }}>Выберите время</h2>
                </div>
                <div className="mb-3">
                  <div style={{ fontSize: "12px", color: "#6B8FA8", marginBottom: "8px" }}>Утро</div>
                  <div className="flex gap-2 flex-wrap">
                    {TIMES_AM.map((t) => (
                      <button
                        key={t}
                        onClick={() => update("time", t)}
                        className="px-4 py-2.5 rounded-xl transition-all"
                        style={{
                          backgroundColor: selected.time === t ? "#1B6CA8" : "#F7F9FC",
                          color: selected.time === t ? "#FFFFFF" : "#4A6480",
                          border: `1px solid ${selected.time === t ? "#1B6CA8" : "#E8EEF4"}`,
                          fontSize: "14px",
                          fontWeight: selected.time === t ? 600 : 400,
                        }}
                      >
                        {t}
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: "12px", color: "#6B8FA8", marginBottom: "8px" }}>День / Вечер</div>
                  <div className="flex gap-2 flex-wrap">
                    {TIMES_PM.map((t) => (
                      <button
                        key={t}
                        onClick={() => update("time", t)}
                        className="px-4 py-2.5 rounded-xl transition-all"
                        style={{
                          backgroundColor: selected.time === t ? "#1B6CA8" : "#F7F9FC",
                          color: selected.time === t ? "#FFFFFF" : "#4A6480",
                          border: `1px solid ${selected.time === t ? "#1B6CA8" : "#E8EEF4"}`,
                          fontSize: "14px",
                          fontWeight: selected.time === t ? 600 : 400,
                        }}
                      >
                        {t}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Step 4 — Patient Info */}
        {step === 4 && (
          <div className="flex flex-col gap-4">
            <div
              className="rounded-2xl p-6"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
            >
              <h2 style={{ fontWeight: 600, fontSize: "17px", color: "#1A2B3C", marginBottom: "4px" }}>
                Ваши данные
              </h2>
              <p style={{ fontSize: "13px", color: "#6B8FA8", marginBottom: "20px" }}>
                Нужны для подтверждения записи
              </p>
              <div className="flex flex-col gap-4">
                <div className="flex flex-col gap-1.5">
                  <label style={{ fontSize: "13px", fontWeight: 500, color: "#4A6480" }}>
                    Имя и фамилия *
                  </label>
                  <div className="relative">
                    <User size={15} className="absolute left-4 top-1/2 -translate-y-1/2" style={{ color: "#6B8FA8" }} />
                    <input
                      type="text"
                      placeholder="Иван Петров"
                      value={selected.name}
                      onChange={(e) => update("name", e.target.value)}
                      className="w-full pl-10 pr-4 py-3 rounded-xl outline-none"
                      style={{ backgroundColor: "#F0F5FA", border: "1px solid #E0EAF3", fontSize: "14px", color: "#1A2B3C" }}
                    />
                  </div>
                </div>
                <div className="flex flex-col gap-1.5">
                  <label style={{ fontSize: "13px", fontWeight: 500, color: "#4A6480" }}>Телефон *</label>
                  <div className="relative">
                    <Phone size={15} className="absolute left-4 top-1/2 -translate-y-1/2" style={{ color: "#6B8FA8" }} />
                    <input
                      type="tel"
                      placeholder="+7 (999) 000-00-00"
                      value={selected.phone}
                      onChange={(e) => update("phone", e.target.value)}
                      className="w-full pl-10 pr-4 py-3 rounded-xl outline-none"
                      style={{ backgroundColor: "#F0F5FA", border: "1px solid #E0EAF3", fontSize: "14px", color: "#1A2B3C" }}
                    />
                  </div>
                </div>
                <div className="flex flex-col gap-1.5">
                  <label style={{ fontSize: "13px", fontWeight: 500, color: "#4A6480" }}>
                    Email <span style={{ color: "#6B8FA8", fontWeight: 400 }}>(необязательно)</span>
                  </label>
                  <div className="relative">
                    <Mail size={15} className="absolute left-4 top-1/2 -translate-y-1/2" style={{ color: "#6B8FA8" }} />
                    <input
                      type="email"
                      placeholder="example@mail.ru"
                      value={selected.email}
                      onChange={(e) => update("email", e.target.value)}
                      className="w-full pl-10 pr-4 py-3 rounded-xl outline-none"
                      style={{ backgroundColor: "#F0F5FA", border: "1px solid #E0EAF3", fontSize: "14px", color: "#1A2B3C" }}
                    />
                  </div>
                </div>
                <div className="flex flex-col gap-1.5">
                  <label style={{ fontSize: "13px", fontWeight: 500, color: "#4A6480" }}>
                    Комментарий <span style={{ color: "#6B8FA8", fontWeight: 400 }}>(необязательно)</span>
                  </label>
                  <textarea
                    placeholder="Опишите проблему или пожелания к врачу..."
                    value={selected.comment}
                    onChange={(e) => update("comment", e.target.value)}
                    rows={3}
                    className="w-full px-4 py-3 rounded-xl outline-none resize-none"
                    style={{ backgroundColor: "#F0F5FA", border: "1px solid #E0EAF3", fontSize: "14px", color: "#1A2B3C" }}
                  />
                </div>
              </div>
            </div>

            {/* Summary */}
            <div
              className="rounded-2xl p-5"
              style={{ backgroundColor: "#EBF4FB", border: "1px solid #D0E6F5" }}
            >
              <div style={{ fontSize: "13px", fontWeight: 600, color: "#1A2B3C", marginBottom: "12px" }}>
                Сводка записи
              </div>
              {[
                { label: "Услуга", value: bookingServices.find((s) => s.id === selected.service)?.name },
                { label: "Врач", value: selected.doctor === "any" ? "Любой доступный" : bookingDoctors.find((d) => String(d.id) === selected.doctor)?.name },
                { label: "Дата и время", value: `${selected.date}, ${selected.time}` },
              ].map((r) => (
                <div key={r.label} className="flex items-center justify-between py-2" style={{ borderBottom: "1px solid #D0E6F5" }}>
                  <span style={{ fontSize: "12px", color: "#6B8FA8" }}>{r.label}</span>
                  <span style={{ fontSize: "13px", fontWeight: 500, color: "#1A2B3C" }}>{r.value}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Navigation buttons */}
        <div className="flex gap-3 mt-6">
          {step > 1 && (
            <button
              onClick={prev}
              className="flex items-center gap-2 px-5 py-3 rounded-xl transition-all"
              style={{ backgroundColor: "#FFFFFF", color: "#4A6480", border: "1px solid #E8EEF4", fontSize: "14px", fontWeight: 500 }}
            >
              <ChevronLeft size={16} />
              Назад
            </button>
          )}
          <button
            onClick={step === 4 ? () => setStep(5 as unknown as Step) : next}
            disabled={!canProceed()}
            className="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl transition-all"
            style={{
              backgroundColor: canProceed() ? "#1B6CA8" : "#D0E6F5",
              color: canProceed() ? "#FFFFFF" : "#6B8FA8",
              fontSize: "14px",
              fontWeight: 600,
              cursor: canProceed() ? "pointer" : "not-allowed",
            }}
          >
            {step === 4 ? "Подтвердить запись" : "Продолжить"}
            {step < 4 && <ChevronRight size={16} />}
            {step === 4 && <Check size={16} />}
          </button>
        </div>

        <p style={{ fontSize: "11px", color: "#6B8FA8", textAlign: "center", marginTop: "12px" }}>
          Нажимая «Подтвердить», вы соглашаетесь с политикой обработки персональных данных
        </p>
      </section>

      <Footer onNavigate={onNavigate} />
    </div>
  );
}
