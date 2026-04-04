import { useEffect, useState } from "react";
import { Page } from "../App";
import { LoyaltyPatientSelectorCard } from "./doctor-cabinet/LoyaltyPatientSelectorCard";
import { ManualAdjustmentForm } from "./doctor-cabinet/ManualAdjustmentForm";
import { OperatorWalletSummaryCard } from "./doctor-cabinet/OperatorWalletSummaryCard";
import { LoyaltyLedgerCard } from "./loyalty/LoyaltyLedgerCard";
import { useManualAdjustment } from "../hooks/useManualAdjustment";
import { usePatientLoyalty } from "../hooks/usePatientLoyalty";
import { loyaltyPilotConfig } from "../services/loyaltyConfig";
import {
  LayoutDashboard,
  Users,
  CalendarCheck,
  ClipboardList,
  Bell,
  LogOut,
  Menu,
  X,
  Clock,
  ChevronRight,
  Check,
  Circle,
  AlertCircle,
  FileText,
  User,
  ChevronDown,
} from "lucide-react";

interface Props {
  onNavigate: (page: Page) => void;
}

const DOCTOR = {
  name: "Игорь Петров",
  role: "Хирург, Имплантолог",
  initials: "ИП",
};

type AppStatus = "waiting" | "in-progress" | "done" | "cancelled";

interface Appointment {
  id: number;
  time: string;
  patient: string;
  age: number;
  service: string;
  status: AppStatus;
  isNew: boolean;
  note?: string;
}

const TODAY_APPOINTMENTS: Appointment[] = [
  { id: 1, time: "09:00", patient: "Анна Кузнецова", age: 34, service: "Консультация имплантолога", status: "done", isNew: false },
  { id: 2, time: "10:30", patient: "Михаил Соловьёв", age: 45, service: "Установка импланта Nobel", status: "done", isNew: false, note: "Аллергия на лидокаин — использовать артикаин" },
  { id: 3, time: "12:00", patient: "Ольга Максимова", age: 28, service: "Удаление зуба мудрости", status: "in-progress", isNew: true },
  { id: 4, time: "14:30", patient: "Сергей Белов", age: 52, service: "Проверка заживления импланта", status: "waiting", isNew: false },
  { id: 5, time: "16:00", patient: "Екатерина Смирнова", age: 38, service: "Консультация + план лечения", status: "waiting", isNew: true },
  { id: 6, time: "17:30", patient: "Дмитрий Фёдоров", age: 41, service: "Костная пластика", status: "waiting", isNew: false },
];

const STATUS_MAP: Record<AppStatus, { label: string; color: string; bg: string; icon: React.ReactNode }> = {
  "waiting":     { label: "Ожидает",      color: "#6B8FA8", bg: "#F0F5FA",  icon: <Circle size={12} />          },
  "in-progress": { label: "На приёме",    color: "#1B6CA8", bg: "#EBF4FB",  icon: <Clock size={12} />           },
  "done":        { label: "Завершён",     color: "#22A05B", bg: "#E6F5ED",  icon: <Check size={12} />           },
  "cancelled":   { label: "Отменён",      color: "#D63B3B", bg: "#FFF0F0",  icon: <X size={12} />               },
};

type NavSection = "dashboard" | "patients" | "schedule" | "notes";

const NAV_ITEMS: { id: NavSection; label: string; icon: React.ElementType }[] = [
  { id: "dashboard",  label: "Сегодня",          icon: LayoutDashboard },
  { id: "patients",   label: "Пациенты",          icon: Users           },
  { id: "schedule",   label: "Расписание",        icon: CalendarCheck   },
  { id: "notes",      label: "Заметки",           icon: ClipboardList   },
];

function StatusBadge({ status }: { status: AppStatus }) {
  const s = STATUS_MAP[status];
  return (
    <span
      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full"
      style={{ backgroundColor: s.bg, color: s.color, fontSize: "11px", fontWeight: 600 }}
    >
      {s.icon}
      {s.label}
    </span>
  );
}

function PatientCard({ apt, onUpdateStatus }: { apt: Appointment; onUpdateStatus: (id: number, s: AppStatus) => void }) {
  const [expanded, setExpanded] = useState(false);
  const [noteText, setNoteText] = useState(apt.note || "");
  const [reco, setReco] = useState("");

  return (
    <div
      className="rounded-2xl overflow-hidden"
      style={{
        backgroundColor: "#FFFFFF",
        border: `1px solid ${apt.status === "in-progress" ? "#1B6CA8" : "#E8EEF4"}`,
        boxShadow: apt.status === "in-progress" ? "0 0 0 3px rgba(27,108,168,0.08)" : "none",
      }}
    >
      <button
        className="w-full flex items-center gap-4 px-5 py-4 text-left"
        onClick={() => setExpanded(!expanded)}
      >
        {/* Time */}
        <div
          className="w-14 shrink-0 text-center rounded-xl py-2"
          style={{ backgroundColor: apt.status === "in-progress" ? "#EBF4FB" : "#F7F9FC" }}
        >
          <div style={{ fontSize: "14px", fontWeight: 700, color: apt.status === "in-progress" ? "#1B6CA8" : "#1A2B3C" }}>
            {apt.time}
          </div>
        </div>

        {/* Patient */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span style={{ fontWeight: 600, fontSize: "14px", color: "#1A2B3C" }}>{apt.patient}</span>
            {apt.isNew && (
              <span
                className="px-2 py-0.5 rounded-full"
                style={{ backgroundColor: "#EBF4FB", color: "#1B6CA8", fontSize: "10px", fontWeight: 600 }}
              >
                Новый
              </span>
            )}
            {apt.note && (
              <AlertCircle size={14} style={{ color: "#E8970A", flexShrink: 0 }} />
            )}
          </div>
          <div style={{ fontSize: "12px", color: "#6B8FA8", marginTop: "2px" }}>
            {apt.service} · {apt.age} лет
          </div>
        </div>

        <StatusBadge status={apt.status} />
        <ChevronDown
          size={16}
          style={{
            color: "#6B8FA8",
            transform: expanded ? "rotate(180deg)" : "rotate(0deg)",
            transition: "transform 0.2s",
            flexShrink: 0,
          }}
        />
      </button>

      {expanded && (
        <div style={{ borderTop: "1px solid #E8EEF4" }} className="px-5 py-4 flex flex-col gap-4">
          {/* Alert note */}
          {apt.note && (
            <div
              className="rounded-xl p-3 flex items-start gap-2.5"
              style={{ backgroundColor: "#FFF8EC", border: "1px solid #FCDEA3" }}
            >
              <AlertCircle size={14} style={{ color: "#E8970A", flexShrink: 0, marginTop: "1px" }} />
              <span style={{ fontSize: "13px", color: "#8A5A00" }}>{apt.note}</span>
            </div>
          )}

          {/* Status change */}
          <div>
            <div style={{ fontSize: "12px", color: "#6B8FA8", marginBottom: "8px", fontWeight: 500 }}>
              Статус приёма
            </div>
            <div className="flex gap-2 flex-wrap">
              {(["waiting", "in-progress", "done"] as AppStatus[]).map((s) => (
                <button
                  key={s}
                  onClick={() => onUpdateStatus(apt.id, s)}
                  className="px-3 py-2 rounded-xl transition-all"
                  style={{
                    backgroundColor: apt.status === s ? STATUS_MAP[s].bg : "#F7F9FC",
                    color: apt.status === s ? STATUS_MAP[s].color : "#4A6480",
                    border: `1px solid ${apt.status === s ? STATUS_MAP[s].color + "60" : "#E8EEF4"}`,
                    fontSize: "12px",
                    fontWeight: apt.status === s ? 600 : 400,
                  }}
                >
                  {STATUS_MAP[s].label}
                </button>
              ))}
            </div>
          </div>

          {/* Note */}
          <div>
            <div style={{ fontSize: "12px", color: "#6B8FA8", marginBottom: "8px", fontWeight: 500 }}>
              Заметка врача
            </div>
            <textarea
              value={noteText}
              onChange={(e) => setNoteText(e.target.value)}
              rows={3}
              placeholder="Добавьте заметку по данному визиту..."
              className="w-full px-4 py-3 rounded-xl outline-none resize-none"
              style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4", fontSize: "13px", color: "#1A2B3C" }}
            />
          </div>

          {/* Recommendations */}
          <div>
            <div style={{ fontSize: "12px", color: "#6B8FA8", marginBottom: "8px", fontWeight: 500 }}>
              Рекомендации пациенту
            </div>
            <textarea
              value={reco}
              onChange={(e) => setReco(e.target.value)}
              rows={2}
              placeholder="Инструкции после лечения, назначения..."
              className="w-full px-4 py-3 rounded-xl outline-none resize-none"
              style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4", fontSize: "13px", color: "#1A2B3C" }}
            />
          </div>

          <div className="flex gap-2">
            <button
              className="flex-1 py-2.5 rounded-xl transition-all"
              style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "13px", fontWeight: 600 }}
            >
              Сохранить
            </button>
            <button
              className="px-4 py-2.5 rounded-xl transition-all"
              style={{ backgroundColor: "#FFF0F0", color: "#D63B3B", fontSize: "13px", fontWeight: 500 }}
            >
              Отменить приём
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export function DoctorCabinet({ onNavigate }: Props) {
  const [activeSection, setActiveSection] = useState<NavSection>("dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [appointments, setAppointments] = useState(TODAY_APPOINTMENTS);
  const [selectedPatientId, setSelectedPatientId] = useState<string | null>(
    loyaltyPilotConfig.operatorPatients[0]?.id ?? null,
  );
  const selectedPatient =
    loyaltyPilotConfig.operatorPatients.find((patient) => patient.id === selectedPatientId) ?? null;
  const {
    wallet: loyaltyWallet,
    ledger: loyaltyLedger,
    loading: loyaltyLoading,
    error: loyaltyError,
    refetch: refetchLoyalty,
  } = usePatientLoyalty(selectedPatientId, activeSection === "patients" && Boolean(selectedPatientId));
  const {
    submitting: adjustmentSubmitting,
    successMessage: adjustmentSuccessMessage,
    errorMessage: adjustmentErrorMessage,
    submitAdjustment,
    clearFeedback,
  } = useManualAdjustment(selectedPatientId, refetchLoyalty);

  useEffect(() => {
    clearFeedback();
  }, [selectedPatientId, clearFeedback]);

  const updateStatus = (id: number, status: AppStatus) => {
    setAppointments((prev) => prev.map((a) => a.id === id ? { ...a, status } : a));
  };

  const stats = {
    total: appointments.length,
    done: appointments.filter((a) => a.status === "done").length,
    inProgress: appointments.filter((a) => a.status === "in-progress").length,
    waiting: appointments.filter((a) => a.status === "waiting").length,
  };

  const renderContent = () => {
    switch (activeSection) {
      case "dashboard":
        return (
          <div className="flex flex-col gap-5">
            {/* Greeting */}
            <div>
              <h1 style={{ fontWeight: 700, fontSize: "22px", color: "#1A2B3C" }}>
                Добрый день, {DOCTOR.name.split(" ")[0]}!
              </h1>
              <p style={{ fontSize: "13px", color: "#6B8FA8", marginTop: "4px" }}>
                Вторник, 7 апреля 2026 · {DOCTOR.role}
              </p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {[
                { label: "Всего сегодня", value: stats.total, color: "#1A2B3C", bg: "#FFFFFF" },
                { label: "Завершено", value: stats.done, color: "#22A05B", bg: "#E6F5ED" },
                { label: "На приёме", value: stats.inProgress, color: "#1B6CA8", bg: "#EBF4FB" },
                { label: "Ожидают", value: stats.waiting, color: "#6B8FA8", bg: "#F7F9FC" },
              ].map((s, i) => (
                <div
                  key={i}
                  className="rounded-2xl p-4 text-center"
                  style={{ backgroundColor: s.bg, border: "1px solid #E8EEF4" }}
                >
                  <div style={{ fontSize: "26px", fontWeight: 700, color: s.color }}>{s.value}</div>
                  <div style={{ fontSize: "11px", color: "#6B8FA8", marginTop: "3px" }}>{s.label}</div>
                </div>
              ))}
            </div>

            {/* Appointments */}
            <div>
              <div style={{ fontWeight: 600, fontSize: "16px", color: "#1A2B3C", marginBottom: "12px" }}>
                Расписание на сегодня
              </div>
              <div className="flex flex-col gap-3">
                {appointments.map((apt) => (
                  <PatientCard key={apt.id} apt={apt} onUpdateStatus={updateStatus} />
                ))}
              </div>
            </div>
          </div>
        );

      case "patients":
        return (
          <div className="flex flex-col gap-5">
            <div>
              <h1 style={{ fontWeight: 700, fontSize: "22px", color: "#1A2B3C" }}>
                Пациенты и loyalty-операции
              </h1>
              <p style={{ fontSize: "13px", color: "#6B8FA8", marginTop: "4px", lineHeight: 1.5 }}>
                Внутренний пилотный блок: смотрим реальный бонусный баланс пациента, историю операций и делаем ручную корректировку с аудитом.
              </p>
            </div>

            <LoyaltyPatientSelectorCard
              patients={loyaltyPilotConfig.operatorPatients}
              selectedPatientId={selectedPatientId}
              onSelect={setSelectedPatientId}
            />

            <div className="grid lg:grid-cols-2 gap-5">
              <OperatorWalletSummaryCard
                patientLabel={selectedPatient?.label ?? "Пациент не выбран"}
                wallet={loyaltyWallet}
                loading={loyaltyLoading}
                error={loyaltyError}
              />
              <ManualAdjustmentForm
                patientLabel={selectedPatient?.label ?? "Пациент не выбран"}
                canAdjust={loyaltyPilotConfig.canManageManualAdjustments}
                currentRoleLabel={loyaltyPilotConfig.operatorRoleLabel}
                disabled={!selectedPatientId}
                submitting={adjustmentSubmitting}
                successMessage={adjustmentSuccessMessage}
                errorMessage={adjustmentErrorMessage}
                onSubmit={submitAdjustment}
              />
            </div>

            <LoyaltyLedgerCard
              title="История loyalty-операций пациента"
              entries={loyaltyLedger}
              loading={loyaltyLoading}
              error={loyaltyError}
              emptyTitle="У пациента ещё нет loyalty-операций"
              emptyDescription="После начисления, списания, возврата или ручной корректировки история появится в этом блоке."
            />
          </div>
        );

      case "schedule":
        return (
          <div>
            <h1 style={{ fontWeight: 700, fontSize: "22px", color: "#1A2B3C", marginBottom: "20px" }}>
              Расписание
            </h1>
            <div
              className="rounded-2xl p-6 text-center"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
            >
              <CalendarCheck size={40} className="mx-auto mb-3" style={{ color: "#D0E6F5" }} />
              <div style={{ fontWeight: 600, fontSize: "16px", color: "#1A2B3C", marginBottom: "6px" }}>
                Календарь записей
              </div>
              <p style={{ fontSize: "13px", color: "#6B8FA8" }}>
                Полное расписание по неделям и месяцам
              </p>
            </div>
          </div>
        );

      case "notes":
        return (
          <div>
            <h1 style={{ fontWeight: 700, fontSize: "22px", color: "#1A2B3C", marginBottom: "20px" }}>
              Заметки
            </h1>
            <div
              className="rounded-2xl p-6"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
            >
              <div style={{ fontSize: "13px", color: "#6B8FA8", marginBottom: "12px" }}>
                Общая заметка на день
              </div>
              <textarea
                rows={8}
                placeholder="Заметки, напоминания, важные детали на сегодня..."
                className="w-full px-4 py-3 rounded-xl outline-none resize-none"
                style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4", fontSize: "14px", color: "#1A2B3C" }}
              />
              <button
                className="mt-3 px-5 py-2.5 rounded-xl transition-all"
                style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "13px", fontWeight: 600 }}
              >
                Сохранить заметку
              </button>
            </div>
          </div>
        );
    }
  };

  return (
    <div
      className="min-h-screen flex flex-col"
      style={{ fontFamily: "'Inter', sans-serif", backgroundColor: "#F7F9FC" }}
    >
      {/* Top bar — doctor variant */}
      <header
        className="sticky top-0 z-40 flex items-center justify-between px-4 md:px-6 h-14"
        style={{ backgroundColor: "#1A2B3C", borderBottom: "1px solid rgba(255,255,255,0.08)" }}
      >
        <div className="flex items-center gap-3">
          <button
            className="md:hidden p-2 rounded-lg"
            style={{ color: "rgba(255,255,255,0.7)" }}
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
          <div className="flex items-center gap-2">
            <div
              className="w-7 h-7 rounded-lg flex items-center justify-center"
              style={{ backgroundColor: "#2A5A8A" }}
            >
              <span style={{ color: "#fff", fontSize: "11px", fontWeight: 700 }}>A</span>
            </div>
            <span style={{ fontWeight: 700, fontSize: "14px", color: "#FFFFFF" }}>Aster Dental</span>
            <span
              className="hidden sm:inline px-2 py-0.5 rounded-full"
              style={{ backgroundColor: "rgba(255,255,255,0.12)", color: "#7AAECA", fontSize: "11px", fontWeight: 500 }}
            >
              Кабинет врача
            </span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            className="relative p-2 rounded-lg"
            style={{ color: "rgba(255,255,255,0.6)" }}
          >
            <Bell size={16} />
            <div className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full" style={{ backgroundColor: "#4FC3D4" }} />
          </button>
          <button
            onClick={() => onNavigate("public")}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg"
            style={{ backgroundColor: "rgba(255,255,255,0.08)", color: "rgba(255,255,255,0.6)", fontSize: "12px" }}
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
            style={{ backgroundColor: "rgba(26,43,60,0.5)" }}
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
          {/* Doctor profile */}
          <div
            className="p-4 mx-3 mt-3 rounded-xl"
            style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4" }}
          >
            <div className="flex items-center gap-3">
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
                style={{ backgroundColor: "#1A2B3C" }}
              >
                <span style={{ color: "#fff", fontWeight: 700, fontSize: "14px" }}>{DOCTOR.initials}</span>
              </div>
              <div className="min-w-0">
                <div style={{ fontWeight: 600, fontSize: "13px", color: "#1A2B3C" }} className="truncate">
                  {DOCTOR.name}
                </div>
                <div style={{ fontSize: "11px", color: "#6B8FA8", marginTop: "1px" }} className="truncate">
                  {DOCTOR.role}
                </div>
              </div>
            </div>
          </div>

          {/* Today stats mini */}
          <div className="px-3 py-3">
            <div
              className="rounded-xl px-4 py-3 flex items-center justify-between"
              style={{ backgroundColor: "#EBF4FB" }}
            >
              <div>
                <div style={{ fontSize: "11px", color: "#6B8FA8" }}>Сегодня</div>
                <div style={{ fontSize: "18px", fontWeight: 700, color: "#1B6CA8" }}>
                  {stats.done}/{stats.total}
                </div>
              </div>
              <div style={{ fontSize: "11px", color: "#4A6480", textAlign: "right" }}>
                <div style={{ color: "#22A05B", fontWeight: 500 }}>✓ {stats.done} завершено</div>
                <div style={{ color: "#1B6CA8" }}>⏳ {stats.waiting} ожидают</div>
              </div>
            </div>
          </div>

          {/* Nav */}
          <nav className="flex-1 px-3 flex flex-col gap-0.5 overflow-y-auto">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = activeSection === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => { setActiveSection(item.id); setSidebarOpen(false); }}
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

          {/* Bottom links */}
          <div className="p-3 flex flex-col gap-1" style={{ borderTop: "1px solid #E8EEF4" }}>
            <button
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl w-full text-left"
              style={{ color: "#4A6480" }}
            >
              <FileText size={15} />
              <span style={{ fontSize: "13px" }}>Документация</span>
            </button>
            <button
              onClick={() => onNavigate("public")}
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl w-full text-left"
              style={{ color: "#D63B3B" }}
            >
              <LogOut size={15} />
              <span style={{ fontSize: "13px", fontWeight: 500 }}>Выйти</span>
            </button>
          </div>
        </aside>

        {/* Main */}
        <main className="flex-1 min-w-0 p-4 md:p-6 overflow-y-auto">
          <div className="max-w-3xl mx-auto">{renderContent()}</div>
        </main>
      </div>
    </div>
  );
}
