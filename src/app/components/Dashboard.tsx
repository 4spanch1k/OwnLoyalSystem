import { useState } from "react";
import { Page } from "../App";
import {
  LayoutDashboard,
  User,
  Globe,
  Moon,
  CalendarCheck,
  CalendarPlus,
  LogOut,
  Gift,
  CreditCard,
  Stethoscope,
  Bell,
  ChevronRight,
  Star,
  Clock,
  Check,
  Menu,
  X,
  TrendingUp,
  AlertCircle,
} from "lucide-react";

/* ── Types ── */
interface Appointment {
  id: number;
  doctor: string;
  specialty: string;
  date: string;
  time: string;
  status: "upcoming" | "completed" | "cancelled";
}

interface Payment {
  id: number;
  service: string;
  date: string;
  amount: number;
  status: "paid" | "pending";
}

interface Service {
  id: number;
  name: string;
  visits: number;
  lastDate: string;
  icon: string;
}

/* ── Mock data ── */
const PATIENT = {
  name: "Анна",
  fullName: "Анна Сергеевна Кузнецова",
  email: "anna.kuznetsova@mail.ru",
  phone: "+7 (916) 445-22-33",
  bonus: 1240,
  bonusLevel: "Серебряный",
  nextLevel: 2000,
};

const APPOINTMENTS: Appointment[] = [
  { id: 1, doctor: "Марина Соколова", specialty: "Терапевт", date: "4 апреля 2026", time: "14:30", status: "upcoming" },
  { id: 2, doctor: "Дмитрий Волков", specialty: "Ортодонт", date: "18 апреля 2026", time: "11:00", status: "upcoming" },
  { id: 3, doctor: "Марина Соколова", specialty: "Терапевт", date: "10 марта 2026", time: "10:00", status: "completed" },
  { id: 4, doctor: "Елена Кравцова", specialty: "Гигиенист", date: "15 января 2026", time: "09:30", status: "completed" },
];

const PAYMENTS: Payment[] = [
  { id: 1, service: "Лечение кариеса (2 зуба)", date: "10 марта 2026", amount: 7800, status: "paid" },
  { id: 2, service: "Профессиональная чистка", date: "15 января 2026", amount: 3200, status: "paid" },
  { id: 3, service: "Консультация ортодонта", date: "20 декабря 2025", amount: 1500, status: "paid" },
  { id: 4, service: "Рентген (панорамный)", date: "20 декабря 2025", amount: 900, status: "paid" },
];

const SERVICES: Service[] = [
  { id: 1, name: "Лечение кариеса", visits: 3, lastDate: "10 марта 2026", icon: "🦷" },
  { id: 2, name: "Профчистка зубов", visits: 2, lastDate: "15 января 2026", icon: "✨" },
  { id: 3, name: "Рентгенография", visits: 2, lastDate: "20 декабря 2025", icon: "📷" },
  { id: 4, name: "Консультация", visits: 1, lastDate: "20 декабря 2025", icon: "💬" },
];

type NavSection = "main" | "account" | "language" | "theme" | "appointments" | "book";

const NAV_ITEMS: { id: NavSection; label: string; icon: React.ElementType }[] = [
  { id: "main", label: "Мой кабинет", icon: LayoutDashboard },
  { id: "account", label: "Данные аккаунта", icon: User },
  { id: "language", label: "Язык интерфейса", icon: Globe },
  { id: "theme", label: "Тема", icon: Moon },
  { id: "appointments", label: "Мои записи", icon: CalendarCheck },
  { id: "book", label: "Записаться", icon: CalendarPlus },
];

/* ── Sub-components ── */
function BonusCard() {
  const progress = (PATIENT.bonus / PATIENT.nextLevel) * 100;
  return (
    <div
      className="rounded-2xl p-5 relative overflow-hidden"
      style={{ background: "linear-gradient(135deg, #1B6CA8 0%, #0F4C7A 100%)" }}
    >
      <div className="absolute -right-8 -top-8 w-32 h-32 rounded-full opacity-10" style={{ backgroundColor: "#FFFFFF" }} />
      <div className="absolute -right-2 bottom-4 w-16 h-16 rounded-full opacity-5" style={{ backgroundColor: "#FFFFFF" }} />
      <div className="flex items-start justify-between mb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Gift size={15} color="rgba(255,255,255,0.8)" />
            <span style={{ fontSize: "12px", color: "rgba(255,255,255,0.7)", fontWeight: 500 }}>Мои бонусы</span>
          </div>
          <div style={{ fontSize: "32px", fontWeight: 700, color: "#FFFFFF", lineHeight: 1 }}>
            {PATIENT.bonus.toLocaleString("ru")}
          </div>
          <div style={{ fontSize: "12px", color: "rgba(255,255,255,0.6)", marginTop: "2px" }}>бонусных баллов</div>
        </div>
        <div
          className="px-3 py-1.5 rounded-full flex items-center gap-1"
          style={{ backgroundColor: "rgba(255,255,255,0.15)" }}
        >
          <Star size={11} color="#FFD166" />
          <span style={{ fontSize: "11px", color: "#FFFFFF", fontWeight: 500 }}>{PATIENT.bonusLevel}</span>
        </div>
      </div>
      <div>
        <div className="flex justify-between mb-1.5">
          <span style={{ fontSize: "11px", color: "rgba(255,255,255,0.6)" }}>До уровня «Золотой»</span>
          <span style={{ fontSize: "11px", color: "rgba(255,255,255,0.8)", fontWeight: 500 }}>
            {PATIENT.bonus} / {PATIENT.nextLevel}
          </span>
        </div>
        <div className="h-1.5 rounded-full" style={{ backgroundColor: "rgba(255,255,255,0.15)" }}>
          <div className="h-full rounded-full" style={{ width: `${progress}%`, backgroundColor: "#4FC3D4" }} />
        </div>
        <p style={{ fontSize: "11px", color: "rgba(255,255,255,0.5)", marginTop: "6px" }}>
          Ещё {PATIENT.nextLevel - PATIENT.bonus} баллов до следующего уровня
        </p>
      </div>
    </div>
  );
}

function UpcomingAppointments({ onBook }: { onBook: () => void }) {
  const upcoming = APPOINTMENTS.filter((a) => a.status === "upcoming");
  return (
    <div className="rounded-2xl p-5" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <CalendarCheck size={16} style={{ color: "#1B6CA8" }} />
          <span style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>Ближайшие записи</span>
        </div>
        <span
          className="px-2 py-0.5 rounded-full"
          style={{ backgroundColor: "#EBF4FB", color: "#1B6CA8", fontSize: "11px", fontWeight: 600 }}
        >
          {upcoming.length}
        </span>
      </div>
      {upcoming.length === 0 ? (
        <div className="text-center py-6" style={{ color: "#6B8FA8" }}>
          <CalendarCheck size={32} className="mx-auto mb-2 opacity-30" />
          <p style={{ fontSize: "13px" }}>Нет ближайших записей</p>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {upcoming.map((a) => (
            <div key={a.id} className="rounded-xl p-4" style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4" }}>
              <div className="flex items-center justify-between">
                <div>
                  <div style={{ fontWeight: 600, fontSize: "14px", color: "#1A2B3C" }}>{a.doctor}</div>
                  <div style={{ fontSize: "12px", color: "#6B8FA8", marginTop: "2px" }}>{a.specialty}</div>
                </div>
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: "#4FC3D4" }} />
              </div>
              <div className="flex items-center gap-4 mt-3">
                <div className="flex items-center gap-1.5" style={{ color: "#4A6480" }}>
                  <CalendarCheck size={13} />
                  <span style={{ fontSize: "12px" }}>{a.date}</span>
                </div>
                <div className="flex items-center gap-1.5" style={{ color: "#4A6480" }}>
                  <Clock size={13} />
                  <span style={{ fontSize: "12px" }}>{a.time}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      <button
        onClick={onBook}
        className="w-full mt-4 py-3 rounded-xl transition-all flex items-center justify-center gap-2"
        style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}
      >
        <CalendarPlus size={16} />
        Записаться на приём
      </button>
    </div>
  );
}

function PaymentsCard() {
  const total = PAYMENTS.reduce((s, p) => s + p.amount, 0);
  return (
    <div className="rounded-2xl p-5" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
      <div className="flex items-center gap-2 mb-4">
        <CreditCard size={16} style={{ color: "#1B6CA8" }} />
        <span style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>Мои платежи</span>
      </div>
      <div className="rounded-xl p-4 mb-4 flex items-center gap-3" style={{ backgroundColor: "#F0F5FA" }}>
        <TrendingUp size={18} style={{ color: "#1B6CA8" }} />
        <div>
          <div style={{ fontSize: "11px", color: "#6B8FA8" }}>Всего потрачено</div>
          <div style={{ fontSize: "20px", fontWeight: 700, color: "#1A2B3C" }}>
            {total.toLocaleString("ru")} ₽
          </div>
        </div>
      </div>
      <div className="flex flex-col gap-2">
        {PAYMENTS.slice(0, 3).map((p) => (
          <div
            key={p.id}
            className="flex items-center justify-between py-2"
            style={{ borderBottom: "1px solid #F0F5FA" }}
          >
            <div>
              <div style={{ fontSize: "13px", fontWeight: 500, color: "#1A2B3C" }}>{p.service}</div>
              <div style={{ fontSize: "11px", color: "#6B8FA8", marginTop: "1px" }}>{p.date}</div>
            </div>
            <div className="flex items-center gap-2">
              <span style={{ fontSize: "13px", fontWeight: 600, color: "#1A2B3C" }}>
                {p.amount.toLocaleString("ru")} ₽
              </span>
              <div className="w-5 h-5 rounded-full flex items-center justify-center" style={{ backgroundColor: "#E6F5ED" }}>
                <Check size={10} color="#22A05B" />
              </div>
            </div>
          </div>
        ))}
      </div>
      <button
        className="w-full mt-3 py-2.5 rounded-xl transition-all"
        style={{ backgroundColor: "#F0F5FA", color: "#1B6CA8", fontSize: "13px", fontWeight: 500 }}
      >
        Вся история платежей
      </button>
    </div>
  );
}

function ServicesCard() {
  return (
    <div className="rounded-2xl p-5" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
      <div className="flex items-center gap-2 mb-4">
        <Stethoscope size={16} style={{ color: "#1B6CA8" }} />
        <span style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>Мои услуги</span>
      </div>
      <div className="grid grid-cols-2 gap-3">
        {SERVICES.map((s) => (
          <div
            key={s.id}
            className="rounded-xl p-3.5"
            style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4" }}
          >
            <div className="text-xl mb-2">{s.icon}</div>
            <div style={{ fontWeight: 500, fontSize: "13px", color: "#1A2B3C", lineHeight: 1.3 }}>{s.name}</div>
            <div
              className="mt-1.5 inline-flex items-center gap-1 px-2 py-0.5 rounded-full"
              style={{ backgroundColor: "#EBF4FB" }}
            >
              <span style={{ fontSize: "10px", color: "#1B6CA8", fontWeight: 500 }}>
                {s.visits} {s.visits === 1 ? "визит" : "визита"}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function AppointmentsTab() {
  const [tab, setTab] = useState<"upcoming" | "past">("upcoming");
  const upcoming = APPOINTMENTS.filter((a) => a.status === "upcoming");
  const past = APPOINTMENTS.filter((a) => a.status === "completed");
  const list = tab === "upcoming" ? upcoming : past;

  return (
    <div>
      <div className="flex gap-2 mb-5">
        {(["upcoming", "past"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className="px-4 py-2 rounded-xl text-sm transition-all"
            style={{
              backgroundColor: tab === t ? "#1B6CA8" : "#FFFFFF",
              color: tab === t ? "#FFFFFF" : "#4A6480",
              border: `1px solid ${tab === t ? "#1B6CA8" : "#E8EEF4"}`,
              fontWeight: tab === t ? 600 : 400,
              fontSize: "13px",
            }}
          >
            {t === "upcoming" ? `Предстоящие (${upcoming.length})` : `История (${past.length})`}
          </button>
        ))}
      </div>
      <div className="flex flex-col gap-3">
        {list.map((a) => (
          <div
            key={a.id}
            className="rounded-2xl p-5"
            style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
          >
            <div className="flex items-start justify-between">
              <div>
                <div style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>{a.doctor}</div>
                <div style={{ fontSize: "13px", color: "#6B8FA8", marginTop: "2px" }}>{a.specialty}</div>
              </div>
              <div
                className="px-2.5 py-1 rounded-full"
                style={{
                  backgroundColor: a.status === "upcoming" ? "#EBF4FB" : "#E6F5ED",
                  color: a.status === "upcoming" ? "#1B6CA8" : "#22A05B",
                  fontSize: "11px",
                  fontWeight: 500,
                }}
              >
                {a.status === "upcoming" ? "Предстоит" : "Завершён"}
              </div>
            </div>
            <div className="flex items-center gap-5 mt-3">
              <div className="flex items-center gap-1.5" style={{ color: "#4A6480" }}>
                <CalendarCheck size={14} />
                <span style={{ fontSize: "13px" }}>{a.date}</span>
              </div>
              <div className="flex items-center gap-1.5" style={{ color: "#4A6480" }}>
                <Clock size={14} />
                <span style={{ fontSize: "13px" }}>{a.time}</span>
              </div>
            </div>
            {a.status === "upcoming" && (
              <button
                className="mt-3 px-4 py-2 rounded-xl"
                style={{ backgroundColor: "#FFF0F0", color: "#D63B3B", fontSize: "12px", fontWeight: 500 }}
              >
                Отменить запись
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function BookTab() {
  const [step, setStep] = useState(1);
  const [selected, setSelected] = useState({ specialty: "", doctor: "", date: "", time: "" });

  const specialties = ["Терапевт", "Ортодонт", "Хирург", "Гигиенист", "Имплантолог"];
  const doctors = ["Марина Соколова", "Дмитрий Волков", "Елена Кравцова", "Игорь Петров"];
  const dates = ["7 апреля", "8 апреля", "9 апреля", "10 апреля", "11 апреля"];
  const times = ["09:00", "10:30", "12:00", "14:30", "16:00", "17:30"];

  if (step === 3) {
    return (
      <div
        className="rounded-2xl p-8 text-center"
        style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
      >
        <div
          className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
          style={{ backgroundColor: "#E6F5ED" }}
        >
          <Check size={28} color="#22A05B" />
        </div>
        <h2 style={{ fontWeight: 700, fontSize: "20px", color: "#1A2B3C", marginBottom: "8px" }}>
          Запись подтверждена!
        </h2>
        <p style={{ fontSize: "14px", color: "#6B8FA8", marginBottom: "20px" }}>
          Вы записаны к <strong style={{ color: "#1A2B3C" }}>{selected.doctor}</strong>
          <br />
          {selected.date} в {selected.time}
        </p>
        <button
          onClick={() => { setStep(1); setSelected({ specialty: "", doctor: "", date: "", time: "" }); }}
          className="px-6 py-3 rounded-xl transition-all"
          style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}
        >
          Отлично
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-5">
      <div className="flex items-center gap-3">
        {[1, 2].map((s) => (
          <div key={s} className="flex items-center gap-2">
            <div
              className="w-7 h-7 rounded-full flex items-center justify-center"
              style={{
                backgroundColor: step >= s ? "#1B6CA8" : "#E8EEF4",
                color: step >= s ? "#FFFFFF" : "#6B8FA8",
                fontSize: "12px",
                fontWeight: 600,
              }}
            >
              {s}
            </div>
            <span style={{ fontSize: "12px", color: step >= s ? "#1A2B3C" : "#6B8FA8", fontWeight: step >= s ? 500 : 400 }}>
              {s === 1 ? "Выбор услуги" : "Дата и время"}
            </span>
            {s < 2 && (
              <div className="h-px w-6 mx-1" style={{ backgroundColor: step > s ? "#1B6CA8" : "#E8EEF4" }} />
            )}
          </div>
        ))}
      </div>

      {step === 1 && (
        <div className="rounded-2xl p-5" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
          <h3 style={{ fontWeight: 600, fontSize: "16px", color: "#1A2B3C", marginBottom: "16px" }}>
            Выберите специализацию
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mb-5">
            {specialties.map((sp) => (
              <button
                key={sp}
                onClick={() => setSelected({ ...selected, specialty: sp })}
                className="py-3 px-3 rounded-xl transition-all"
                style={{
                  backgroundColor: selected.specialty === sp ? "#1B6CA8" : "#F7F9FC",
                  color: selected.specialty === sp ? "#FFFFFF" : "#4A6480",
                  border: `1px solid ${selected.specialty === sp ? "#1B6CA8" : "#E8EEF4"}`,
                  fontSize: "13px",
                  fontWeight: selected.specialty === sp ? 600 : 400,
                }}
              >
                {sp}
              </button>
            ))}
          </div>
          {selected.specialty && (
            <>
              <h3 style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C", marginBottom: "12px" }}>
                Выберите врача
              </h3>
              <div className="flex flex-col gap-2">
                {doctors.map((d) => (
                  <button
                    key={d}
                    onClick={() => setSelected({ ...selected, doctor: d })}
                    className="py-3 px-4 rounded-xl text-left flex items-center justify-between transition-all"
                    style={{
                      backgroundColor: selected.doctor === d ? "#EBF4FB" : "#F7F9FC",
                      border: `1px solid ${selected.doctor === d ? "#1B6CA8" : "#E8EEF4"}`,
                    }}
                  >
                    <div>
                      <div style={{ fontSize: "14px", fontWeight: 500, color: "#1A2B3C" }}>{d}</div>
                      <div style={{ fontSize: "12px", color: "#6B8FA8" }}>{selected.specialty}</div>
                    </div>
                    {selected.doctor === d && <Check size={16} color="#1B6CA8" />}
                  </button>
                ))}
              </div>
            </>
          )}
          {selected.specialty && selected.doctor && (
            <button
              onClick={() => setStep(2)}
              className="w-full mt-4 py-3 rounded-xl transition-all"
              style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}
            >
              Далее
            </button>
          )}
        </div>
      )}

      {step === 2 && (
        <div className="rounded-2xl p-5" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
          <h3 style={{ fontWeight: 600, fontSize: "16px", color: "#1A2B3C", marginBottom: "16px" }}>
            Выберите дату
          </h3>
          <div className="flex gap-2 flex-wrap mb-5">
            {dates.map((d) => (
              <button
                key={d}
                onClick={() => setSelected({ ...selected, date: d })}
                className="px-4 py-2.5 rounded-xl transition-all"
                style={{
                  backgroundColor: selected.date === d ? "#1B6CA8" : "#F7F9FC",
                  color: selected.date === d ? "#FFFFFF" : "#4A6480",
                  border: `1px solid ${selected.date === d ? "#1B6CA8" : "#E8EEF4"}`,
                  fontSize: "13px",
                  fontWeight: selected.date === d ? 600 : 400,
                }}
              >
                {d}
              </button>
            ))}
          </div>
          <h3 style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C", marginBottom: "12px" }}>
            Выберите время
          </h3>
          <div className="grid grid-cols-3 gap-2">
            {times.map((t) => (
              <button
                key={t}
                onClick={() => setSelected({ ...selected, time: t })}
                className="py-2.5 rounded-xl transition-all"
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
          <div className="flex gap-3 mt-5">
            <button
              onClick={() => setStep(1)}
              className="flex-1 py-3 rounded-xl transition-all"
              style={{ backgroundColor: "#F7F9FC", color: "#4A6480", fontSize: "14px", fontWeight: 500, border: "1px solid #E8EEF4" }}
            >
              Назад
            </button>
            {selected.date && selected.time && (
              <button
                onClick={() => setStep(3)}
                className="flex-1 py-3 rounded-xl transition-all"
                style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}
              >
                Записаться
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function AccountTab() {
  return (
    <div className="rounded-2xl overflow-hidden" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
      <div className="px-6 py-5" style={{ background: "linear-gradient(135deg, #1B6CA8, #0F4C7A)" }}>
        <div className="flex items-center gap-4">
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center"
            style={{ backgroundColor: "rgba(255,255,255,0.15)" }}
          >
            <span style={{ fontSize: "22px", fontWeight: 700, color: "#FFFFFF" }}>
              {PATIENT.fullName.charAt(0)}
            </span>
          </div>
          <div>
            <div style={{ fontWeight: 600, fontSize: "17px", color: "#FFFFFF" }}>{PATIENT.fullName}</div>
            <div style={{ fontSize: "13px", color: "rgba(255,255,255,0.65)", marginTop: "2px" }}>Пациент клиники</div>
          </div>
        </div>
      </div>
      <div className="p-6 flex flex-col gap-4">
        {[
          { label: "Email", value: PATIENT.email },
          { label: "Телефон", value: PATIENT.phone },
          { label: "Бонусный статус", value: PATIENT.bonusLevel },
        ].map((f) => (
          <div key={f.label}>
            <div style={{ fontSize: "12px", color: "#6B8FA8", marginBottom: "4px" }}>{f.label}</div>
            <div
              className="px-4 py-3 rounded-xl"
              style={{ backgroundColor: "#F7F9FC", fontSize: "14px", color: "#1A2B3C", fontWeight: 500 }}
            >
              {f.value}
            </div>
          </div>
        ))}
        <button
          className="w-full py-3 rounded-xl transition-all mt-2"
          style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}
        >
          Редактировать данные
        </button>
      </div>
    </div>
  );
}

/* ── Main Dashboard ── */
interface Props {
  onNavigate: (page: Page) => void;
}

export function Dashboard({ onNavigate }: Props) {
  const [activeSection, setActiveSection] = useState<NavSection>("main");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleNav = (section: NavSection) => {
    setActiveSection(section);
    setSidebarOpen(false);
  };

  const renderContent = () => {
    switch (activeSection) {
      case "main":
        return (
          <div className="flex flex-col gap-5">
            <div>
              <h1 style={{ fontWeight: 700, fontSize: "22px", color: "#1A2B3C" }}>
                Здравствуйте, {PATIENT.name}! 👋
              </h1>
              <p style={{ fontSize: "13px", color: "#6B8FA8", marginTop: "4px" }}>
                Добро пожаловать в ваш личный кабинет
              </p>
            </div>
            <div
              className="rounded-xl p-4 flex items-start gap-3"
              style={{ backgroundColor: "#FFF8EC", border: "1px solid #FCDEA3" }}
            >
              <AlertCircle size={16} style={{ color: "#E8970A", marginTop: "1px", flexShrink: 0 }} />
              <div>
                <div style={{ fontSize: "13px", fontWeight: 600, color: "#8A5A00" }}>Напоминание о визите</div>
                <div style={{ fontSize: "12px", color: "#A07030", marginTop: "2px" }}>
                  У вас запись к терапевту 4 апреля в 14:30. Не забудьте прийти!
                </div>
              </div>
            </div>
            <BonusCard />
            <div className="grid md:grid-cols-2 gap-5">
              <UpcomingAppointments onBook={() => handleNav("book")} />
              <PaymentsCard />
            </div>
            <ServicesCard />
          </div>
        );
      case "appointments":
        return (
          <div>
            <h1 style={{ fontWeight: 700, fontSize: "22px", color: "#1A2B3C", marginBottom: "20px" }}>Мои записи</h1>
            <AppointmentsTab />
          </div>
        );
      case "book":
        return (
          <div>
            <h1 style={{ fontWeight: 700, fontSize: "22px", color: "#1A2B3C", marginBottom: "20px" }}>
              Записаться на приём
            </h1>
            <BookTab />
          </div>
        );
      case "account":
        return (
          <div>
            <h1 style={{ fontWeight: 700, fontSize: "22px", color: "#1A2B3C", marginBottom: "20px" }}>
              Данные аккаунта
            </h1>
            <AccountTab />
          </div>
        );
      case "language":
        return (
          <div className="rounded-2xl p-6" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
            <h1 style={{ fontWeight: 700, fontSize: "22px", color: "#1A2B3C", marginBottom: "20px" }}>
              Язык интерфейса
            </h1>
            {[
              { code: "ru", label: "Русский", flag: "🇷🇺", active: true },
              { code: "en", label: "English", flag: "🇬🇧", active: false },
              { code: "kz", label: "Қазақша", flag: "🇰🇿", active: false },
            ].map((l) => (
              <div
                key={l.code}
                className="flex items-center justify-between p-4 rounded-xl mb-2 cursor-pointer"
                style={{
                  backgroundColor: l.active ? "#EBF4FB" : "#F7F9FC",
                  border: `1px solid ${l.active ? "#1B6CA8" : "#E8EEF4"}`,
                }}
              >
                <div className="flex items-center gap-3">
                  <span className="text-xl">{l.flag}</span>
                  <span style={{ fontSize: "14px", fontWeight: 500, color: "#1A2B3C" }}>{l.label}</span>
                </div>
                {l.active && <Check size={16} color="#1B6CA8" />}
              </div>
            ))}
          </div>
        );
      case "theme":
        return (
          <div className="rounded-2xl p-6" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
            <h1 style={{ fontWeight: 700, fontSize: "22px", color: "#1A2B3C", marginBottom: "20px" }}>
              Тема оформления
            </h1>
            {[
              { id: "light", label: "Светлая", desc: "Белый фон, синие акценты", active: true },
              { id: "dark", label: "Тёмная", desc: "Тёмный фон, мягкие акценты", active: false },
              { id: "auto", label: "Авто", desc: "Следует за системными настройками", active: false },
            ].map((t) => (
              <div
                key={t.id}
                className="flex items-center justify-between p-4 rounded-xl mb-2 cursor-pointer"
                style={{
                  backgroundColor: t.active ? "#EBF4FB" : "#F7F9FC",
                  border: `1px solid ${t.active ? "#1B6CA8" : "#E8EEF4"}`,
                }}
              >
                <div>
                  <div style={{ fontSize: "14px", fontWeight: 500, color: "#1A2B3C" }}>{t.label}</div>
                  <div style={{ fontSize: "12px", color: "#6B8FA8", marginTop: "2px" }}>{t.desc}</div>
                </div>
                {t.active && <Check size={16} color="#1B6CA8" />}
              </div>
            ))}
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div
      className="min-h-screen flex flex-col"
      style={{ fontFamily: "'Inter', sans-serif", backgroundColor: "#F7F9FC" }}
    >
      {/* Top bar */}
      <header
        className="sticky top-0 z-40 flex items-center justify-between px-4 md:px-6 h-14"
        style={{ backgroundColor: "#FFFFFF", borderBottom: "1px solid #E8EEF4" }}
      >
        <div className="flex items-center gap-3">
          <button
            className="md:hidden p-2 rounded-lg"
            style={{ color: "#1A2B3C" }}
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
          <button onClick={() => onNavigate("public")} className="flex items-center gap-2">
            <div
              className="w-7 h-7 rounded-lg flex items-center justify-center"
              style={{ backgroundColor: "#1B6CA8" }}
            >
              <span style={{ color: "#fff", fontSize: "11px", fontWeight: 700 }}>A</span>
            </div>
            <span style={{ fontWeight: 700, fontSize: "14px", color: "#1A2B3C" }}>Aster Dental</span>
          </button>
        </div>
        <div className="flex items-center gap-2">
          <button
            className="relative p-2 rounded-lg"
            style={{ backgroundColor: "#F7F9FC", color: "#4A6480" }}
          >
            <Bell size={16} />
            <div className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full" style={{ backgroundColor: "#1B6CA8" }} />
          </button>
          <button
            onClick={() => onNavigate("public")}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all"
            style={{ backgroundColor: "#F7F9FC", color: "#D63B3B", fontSize: "12px", fontWeight: 500 }}
          >
            <LogOut size={13} />
            <span className="hidden sm:inline">Выйти</span>
          </button>
        </div>
      </header>

      <div className="flex flex-1 relative">
        {/* Overlay */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 z-30 md:hidden"
            style={{ backgroundColor: "rgba(26,43,60,0.4)" }}
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Sidebar */}
        <aside
          className={`fixed md:sticky top-14 left-0 z-30 flex flex-col transition-transform duration-300 md:translate-x-0 ${sidebarOpen ? "translate-x-0" : "-translate-x-full"}`}
          style={{
            width: "240px",
            height: "calc(100vh - 56px)",
            backgroundColor: "#FFFFFF",
            borderRight: "1px solid #E8EEF4",
            flexShrink: 0,
          }}
        >
          <div className="p-4 mx-3 mt-3 rounded-xl" style={{ backgroundColor: "#EBF4FB" }}>
            <div className="flex items-center gap-3">
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
                style={{ backgroundColor: "#1B6CA8" }}
              >
                <span style={{ color: "#fff", fontWeight: 700, fontSize: "15px" }}>{PATIENT.name.charAt(0)}</span>
              </div>
              <div className="min-w-0">
                <div style={{ fontWeight: 600, fontSize: "13px", color: "#1A2B3C" }} className="truncate">
                  {PATIENT.fullName}
                </div>
                <div className="flex items-center gap-1 mt-0.5" style={{ fontSize: "11px", color: "#1B6CA8" }}>
                  <Star size={9} />
                  {PATIENT.bonusLevel}
                </div>
              </div>
            </div>
          </div>

          <nav className="flex-1 px-3 py-4 flex flex-col gap-0.5 overflow-y-auto">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = activeSection === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNav(item.id)}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-xl w-full text-left transition-all"
                  style={{
                    backgroundColor: isActive ? "#EBF4FB" : "transparent",
                    color: isActive ? "#1B6CA8" : "#4A6480",
                  }}
                >
                  <Icon size={16} />
                  <span style={{ fontSize: "13px", fontWeight: isActive ? 600 : 400 }}>{item.label}</span>
                  {isActive && <ChevronRight size={14} className="ml-auto" style={{ color: "#1B6CA8" }} />}
                </button>
              );
            })}
          </nav>

          <div className="p-3" style={{ borderTop: "1px solid #E8EEF4" }}>
            <button
              onClick={() => onNavigate("public")}
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl w-full text-left transition-all"
              style={{ color: "#D63B3B" }}
            >
              <LogOut size={16} />
              <span style={{ fontSize: "13px", fontWeight: 500 }}>Выйти из аккаунта</span>
            </button>
          </div>
        </aside>

        {/* Main content */}
        <main className="flex-1 min-w-0 p-4 md:p-6 overflow-y-auto">
          <div className="max-w-3xl mx-auto">{renderContent()}</div>
        </main>
      </div>
    </div>
  );
}