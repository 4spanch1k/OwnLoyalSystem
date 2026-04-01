import { useState } from "react";
import { Page } from "../App";
import { Header } from "./shared/Header";
import { Footer } from "./shared/Footer";
import {
  Eye,
  EyeOff,
  ChevronDown,
  Star,
  Clock,
  Shield,
  Smile,
  ArrowRight,
  Check,
} from "lucide-react";

const CLINIC_IMAGE =
  "https://images.unsplash.com/photo-1704455306251-b4634215d98f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBkZW50YWwlMjBjbGluaWMlMjBpbnRlcmlvciUyMG1pbmltYWwlMjB3aGl0ZXxlbnwxfHx8fDE3NzQ5NTI3MDd8MA&ixlib=rb-4.1.0&q=80&w=1080";

interface Props {
  onNavigate: (page: Page) => void;
}

export function PublicPage({ onNavigate }: Props) {
  const [activeTab, setActiveTab] = useState<"login" | "register">("login");
  const [showPassword, setShowPassword] = useState(false);
  const [showStaffPassword, setShowStaffPassword] = useState(false);

  const [loginForm, setLoginForm] = useState({ email: "", password: "" });
  const [registerForm, setRegisterForm] = useState({ email: "", phone: "", password: "" });
  const [staffForm, setStaffForm] = useState({ email: "", password: "" });

  const goToCabinet = (e: React.FormEvent) => {
    e.preventDefault();
    onNavigate("cabinet");
  };

  const goToDoctor = (e: React.FormEvent) => {
    e.preventDefault();
    onNavigate("doctor-cabinet");
  };

  return (
    <div
      className="min-h-screen"
      style={{ fontFamily: "'Inter', sans-serif", backgroundColor: "#F7F9FC", color: "#1A2B3C" }}
    >
      <Header onNavigate={onNavigate} activePage="public" />

      {/* ───── HERO ───── */}
      <section className="relative overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `url(${CLINIC_IMAGE})`,
            backgroundSize: "cover",
            backgroundPosition: "center top",
            filter: "brightness(0.35)",
          }}
        />
        <div
          className="absolute inset-0"
          style={{ background: "linear-gradient(135deg, rgba(27,108,168,0.85) 0%, rgba(26,43,60,0.75) 100%)" }}
        />
        <div className="relative max-w-5xl mx-auto px-5 py-16 md:py-24">
          <div className="max-w-lg">
            <div
              className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full mb-5"
              style={{ backgroundColor: "rgba(255,255,255,0.15)", backdropFilter: "blur(8px)" }}
            >
              <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: "#4FC3D4" }} />
              <span style={{ color: "#C8E6F5", fontSize: "12px", fontWeight: 500 }}>
                Принимаем пациентов ежедневно
              </span>
            </div>
            <h1
              style={{
                fontSize: "clamp(26px, 5vw, 40px)",
                fontWeight: 700,
                color: "#FFFFFF",
                lineHeight: 1.25,
                marginBottom: "16px",
              }}
            >
              Забота о вашей улыбке — наша главная задача
            </h1>
            <p style={{ color: "#B8D4E8", fontSize: "15px", lineHeight: 1.7, marginBottom: "28px" }}>
              Современная стоматология с опытными врачами, передовым оборудованием и индивидуальным подходом.
            </p>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => onNavigate("booking")}
                className="inline-flex items-center gap-2 px-6 py-3 rounded-xl transition-all"
                style={{ backgroundColor: "#FFFFFF", color: "#1B6CA8", fontSize: "14px", fontWeight: 600 }}
              >
                Записаться на приём
                <ArrowRight size={16} />
              </button>
              <a
                href="#auth"
                className="inline-flex items-center gap-2 px-6 py-3 rounded-xl transition-all"
                style={{
                  backgroundColor: "rgba(255,255,255,0.12)",
                  color: "#FFFFFF",
                  fontSize: "14px",
                  fontWeight: 500,
                  border: "1px solid rgba(255,255,255,0.2)",
                }}
              >
                Войти в кабинет
                <ChevronDown size={16} />
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* ───── FEATURES ───── */}
      <section className="max-w-5xl mx-auto px-5 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { icon: <Shield size={18} />, label: "Безопасно", sub: "Стерильность и стандарты" },
            { icon: <Star size={18} />, label: "4.9 / 5", sub: "Оценка пациентов" },
            { icon: <Clock size={18} />, label: "Пн–Вс", sub: "Без выходных" },
            { icon: <Smile size={18} />, label: "1 200+", sub: "Довольных пациентов" },
          ].map((f, i) => (
            <div
              key={i}
              className="rounded-2xl p-4 flex flex-col gap-2"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
            >
              <div
                className="w-9 h-9 rounded-xl flex items-center justify-center"
                style={{ backgroundColor: "#EBF4FB", color: "#1B6CA8" }}
              >
                {f.icon}
              </div>
              <div style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>{f.label}</div>
              <div style={{ fontSize: "12px", color: "#6B8FA8" }}>{f.sub}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ───── QUICK NAV ───── */}
      <section className="max-w-5xl mx-auto px-5 pb-10">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { label: "Наши услуги", sub: "Полный спектр лечения", page: "services" as Page, icon: "🦷" },
            { label: "Врачи клиники", sub: "Опытные специалисты", page: "doctors" as Page, icon: "👨‍⚕️" },
            { label: "Цены", sub: "Прозрачная стоимость", page: "prices" as Page, icon: "💳" },
            { label: "Контакты", sub: "Адрес и расписание", page: "contacts" as Page, icon: "📍" },
          ].map((item) => (
            <button
              key={item.page}
              onClick={() => onNavigate(item.page)}
              className="rounded-2xl p-4 text-left flex flex-col gap-2 transition-all group"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}
            >
              <span className="text-2xl">{item.icon}</span>
              <div style={{ fontWeight: 600, fontSize: "14px", color: "#1A2B3C" }}>{item.label}</div>
              <div style={{ fontSize: "12px", color: "#6B8FA8" }}>{item.sub}</div>
              <div className="flex items-center gap-1 mt-1" style={{ color: "#1B6CA8", fontSize: "12px", fontWeight: 500 }}>
                Перейти <ArrowRight size={12} />
              </div>
            </button>
          ))}
        </div>
      </section>

      {/* ───── AUTH ───── */}
      <section id="auth" className="max-w-5xl mx-auto px-5 pb-12">
        <div className="text-center mb-8">
          <h2 style={{ fontWeight: 700, fontSize: "clamp(20px, 3vw, 28px)", color: "#1A2B3C", marginBottom: "8px" }}>
            Личный кабинет пациента
          </h2>
          <p style={{ fontSize: "14px", color: "#6B8FA8" }}>
            Войдите или зарегистрируйтесь, чтобы управлять записями и просматривать историю лечения
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 items-start">
          {/* Patient Auth Card */}
          <div
            className="rounded-3xl overflow-hidden"
            style={{
              backgroundColor: "#FFFFFF",
              border: "1px solid #E8EEF4",
              boxShadow: "0 4px 24px rgba(27,108,168,0.06)",
            }}
          >
            <div
              className="flex"
              style={{ borderBottom: "1px solid #E8EEF4", backgroundColor: "#F7F9FC" }}
            >
              {(["login", "register"] as const).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className="flex-1 py-4 relative transition-all"
                  style={{
                    color: activeTab === tab ? "#1B6CA8" : "#6B8FA8",
                    backgroundColor: activeTab === tab ? "#FFFFFF" : "transparent",
                    fontWeight: activeTab === tab ? 600 : 400,
                    fontSize: "14px",
                  }}
                >
                  {tab === "login" ? "Вход" : "Регистрация"}
                  {activeTab === tab && (
                    <div className="absolute bottom-0 left-0 right-0 h-0.5" style={{ backgroundColor: "#1B6CA8" }} />
                  )}
                </button>
              ))}
            </div>

            <div className="p-6">
              <div className="mb-5">
                <h2 style={{ fontWeight: 600, fontSize: "18px", color: "#1A2B3C", marginBottom: "4px" }}>
                  {activeTab === "login" ? "Добро пожаловать" : "Создать аккаунт"}
                </h2>
                <p style={{ fontSize: "13px", color: "#6B8FA8" }}>
                  {activeTab === "login"
                    ? "Войдите в личный кабинет пациента"
                    : "Зарегистрируйтесь для записи и отслеживания лечения"}
                </p>
              </div>

              {activeTab === "login" ? (
                <form onSubmit={goToCabinet} className="flex flex-col gap-4">
                  <div className="flex flex-col gap-1.5">
                    <label style={{ fontSize: "13px", fontWeight: 500, color: "#4A6480" }}>Email</label>
                    <input
                      type="email"
                      placeholder="example@mail.ru"
                      value={loginForm.email}
                      onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl outline-none transition-all"
                      style={{ backgroundColor: "#F0F5FA", border: "1px solid #E0EAF3", fontSize: "14px", color: "#1A2B3C" }}
                    />
                  </div>
                  <div className="flex flex-col gap-1.5">
                    <label style={{ fontSize: "13px", fontWeight: 500, color: "#4A6480" }}>Пароль</label>
                    <div className="relative">
                      <input
                        type={showPassword ? "text" : "password"}
                        placeholder="••••••••"
                        value={loginForm.password}
                        onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                        className="w-full px-4 py-3 rounded-xl outline-none pr-12"
                        style={{ backgroundColor: "#F0F5FA", border: "1px solid #E0EAF3", fontSize: "14px", color: "#1A2B3C" }}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3.5 top-1/2 -translate-y-1/2"
                        style={{ color: "#6B8FA8" }}
                      >
                        {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                      </button>
                    </div>
                  </div>
                  <div className="flex justify-end">
                    <a href="#" style={{ fontSize: "13px", color: "#1B6CA8", fontWeight: 500 }}>Забыли пароль?</a>
                  </div>
                  <button
                    type="submit"
                    className="w-full py-3 rounded-xl transition-all mt-1"
                    style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}
                  >
                    Войти в кабинет
                  </button>
                </form>
              ) : (
                <form onSubmit={goToCabinet} className="flex flex-col gap-4">
                  <div className="flex flex-col gap-1.5">
                    <label style={{ fontSize: "13px", fontWeight: 500, color: "#4A6480" }}>Email</label>
                    <input
                      type="email"
                      placeholder="example@mail.ru"
                      value={registerForm.email}
                      onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl outline-none"
                      style={{ backgroundColor: "#F0F5FA", border: "1px solid #E0EAF3", fontSize: "14px", color: "#1A2B3C" }}
                    />
                  </div>
                  <div className="flex flex-col gap-1.5">
                    <label style={{ fontSize: "13px", fontWeight: 500, color: "#4A6480" }}>Телефон</label>
                    <input
                      type="tel"
                      placeholder="+7 (999) 000-00-00"
                      value={registerForm.phone}
                      onChange={(e) => setRegisterForm({ ...registerForm, phone: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl outline-none"
                      style={{ backgroundColor: "#F0F5FA", border: "1px solid #E0EAF3", fontSize: "14px", color: "#1A2B3C" }}
                    />
                  </div>
                  <div className="flex flex-col gap-1.5">
                    <label style={{ fontSize: "13px", fontWeight: 500, color: "#4A6480" }}>Пароль</label>
                    <div className="relative">
                      <input
                        type={showPassword ? "text" : "password"}
                        placeholder="Минимум 8 символов"
                        value={registerForm.password}
                        onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })}
                        className="w-full px-4 py-3 rounded-xl outline-none pr-12"
                        style={{ backgroundColor: "#F0F5FA", border: "1px solid #E0EAF3", fontSize: "14px", color: "#1A2B3C" }}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3.5 top-1/2 -translate-y-1/2"
                        style={{ color: "#6B8FA8" }}
                      >
                        {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                      </button>
                    </div>
                  </div>
                  <p style={{ fontSize: "11px", color: "#6B8FA8", lineHeight: 1.6 }}>
                    Нажимая «Зарегистрироваться», вы соглашаетесь с{" "}
                    <a href="#" style={{ color: "#1B6CA8" }}>условиями использования</a> и{" "}
                    <a href="#" style={{ color: "#1B6CA8" }}>политикой конфиденциальности</a>.
                  </p>
                  <button
                    type="submit"
                    className="w-full py-3 rounded-xl transition-all"
                    style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}
                  >
                    Зарегистрироваться
                  </button>
                </form>
              )}
            </div>
          </div>

          {/* Staff + Info column */}
          <div className="flex flex-col gap-5">
            {/* Staff Login Card */}
            <div
              className="rounded-3xl overflow-hidden"
              style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4", boxShadow: "0 4px 24px rgba(27,108,168,0.06)" }}
            >
              <div
                className="px-6 py-4 flex items-center gap-3"
                style={{ background: "linear-gradient(135deg, #1A2B3C 0%, #1B4A6B 100%)" }}
              >
                <div
                  className="w-8 h-8 rounded-lg flex items-center justify-center"
                  style={{ backgroundColor: "rgba(255,255,255,0.12)" }}
                >
                  <Shield size={15} color="#C8E6F5" />
                </div>
                <div>
                  <div style={{ color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}>Вход для сотрудников</div>
                  <div style={{ color: "#7AAECA", fontSize: "11px" }}>Доступ только для персонала клиники</div>
                </div>
              </div>

              <form onSubmit={goToDoctor} className="p-6 flex flex-col gap-4">
                <div className="flex flex-col gap-1.5">
                  <label style={{ fontSize: "13px", fontWeight: 500, color: "#4A6480" }}>Корпоративный email</label>
                  <input
                    type="email"
                    placeholder="staff@asterdental.ru"
                    value={staffForm.email}
                    onChange={(e) => setStaffForm({ ...staffForm, email: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl outline-none"
                    style={{ backgroundColor: "#F0F5FA", border: "1px solid #E0EAF3", fontSize: "14px", color: "#1A2B3C" }}
                  />
                </div>
                <div className="flex flex-col gap-1.5">
                  <label style={{ fontSize: "13px", fontWeight: 500, color: "#4A6480" }}>Пароль</label>
                  <div className="relative">
                    <input
                      type={showStaffPassword ? "text" : "password"}
                      placeholder="••••••••"
                      value={staffForm.password}
                      onChange={(e) => setStaffForm({ ...staffForm, password: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl outline-none pr-12"
                      style={{ backgroundColor: "#F0F5FA", border: "1px solid #E0EAF3", fontSize: "14px", color: "#1A2B3C" }}
                    />
                    <button
                      type="button"
                      onClick={() => setShowStaffPassword(!showStaffPassword)}
                      className="absolute right-3.5 top-1/2 -translate-y-1/2"
                      style={{ color: "#6B8FA8" }}
                    >
                      {showStaffPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                </div>
                <button
                  type="submit"
                  className="w-full py-3 rounded-xl transition-all"
                  style={{ backgroundColor: "#1A2B3C", color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}
                >
                  Войти как сотрудник
                </button>
              </form>
            </div>

            {/* Benefits brief */}
            <div
              className="rounded-2xl p-5"
              style={{ backgroundColor: "#EBF4FB", border: "1px solid #D0E6F5" }}
            >
              <div style={{ fontSize: "13px", fontWeight: 600, color: "#1A2B3C", marginBottom: "12px" }}>
                Преимущества личного кабинета
              </div>
              {[
                "Онлайн-запись в 2 клика",
                "История посещений и платежей",
                "Бонусная программа",
                "Напоминания о визитах",
              ].map((b) => (
                <div key={b} className="flex items-center gap-2.5 py-2" style={{ borderBottom: "1px solid #D0E6F5" }}>
                  <div
                    className="w-5 h-5 rounded-full flex items-center justify-center shrink-0"
                    style={{ backgroundColor: "#1B6CA8" }}
                  >
                    <Check size={11} color="#FFFFFF" />
                  </div>
                  <span style={{ fontSize: "13px", color: "#1A2B3C" }}>{b}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <Footer onNavigate={onNavigate} />
    </div>
  );
}
