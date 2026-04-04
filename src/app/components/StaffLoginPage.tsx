import { useState } from "react";
import { Eye, EyeOff, Shield, ArrowLeft } from "lucide-react";
import { Page } from "../App";
import { Header } from "./shared/Header";
import { Footer } from "./shared/Footer";

interface Props {
  onNavigate: (page: Page) => void;
}

export function StaffLoginPage({ onNavigate }: Props) {
  const [showPassword, setShowPassword] = useState(false);
  const [staffForm, setStaffForm] = useState({ email: "", password: "" });

  const goToDoctor = (event: React.FormEvent) => {
    event.preventDefault();
    onNavigate("doctor-cabinet");
  };

  return (
    <div
      className="min-h-screen"
      style={{ fontFamily: "'Inter', sans-serif", backgroundColor: "#F7F9FC", color: "#1A2B3C" }}
    >
      <Header onNavigate={onNavigate} activePage="public" />

      <section className="max-w-5xl mx-auto px-5 py-12 md:py-16">
        <div className="max-w-4xl mx-auto grid lg:grid-cols-[minmax(0,0.9fr)_minmax(340px,1.1fr)] gap-6 items-start">
          <div
            className="rounded-3xl p-6 md:p-7"
            style={{ backgroundColor: "#EBF4FB", border: "1px solid #D0E6F5" }}
          >
            <div
              className="w-11 h-11 rounded-2xl flex items-center justify-center mb-5"
              style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF" }}
            >
              <Shield size={20} />
            </div>
            <div style={{ fontSize: "12px", fontWeight: 600, color: "#1B6CA8", marginBottom: "10px" }}>
              Служебный доступ
            </div>
            <h1
              style={{
                fontSize: "clamp(24px, 4vw, 34px)",
                fontWeight: 700,
                color: "#1A2B3C",
                lineHeight: 1.2,
                marginBottom: "14px",
              }}
            >
              Вход для сотрудников клиники
            </h1>
            <p style={{ fontSize: "14px", color: "#5E7B94", lineHeight: 1.7, marginBottom: "24px" }}>
              Используйте корпоративный аккаунт, чтобы открыть внутренний кабинет и работать с пациентами,
              расписанием и бонусной системой.
            </p>
            <div className="flex flex-col gap-3">
              {[
                "Только для персонала клиники",
                "Доступ к внутреннему кабинету и пациентским данным",
                "Отдельный вход от личного кабинета пациента",
              ].map((item) => (
                <div key={item} className="flex items-center gap-2.5">
                  <div
                    className="w-5 h-5 rounded-full flex items-center justify-center shrink-0"
                    style={{ backgroundColor: "#1B6CA8", color: "#FFFFFF", fontSize: "11px", fontWeight: 700 }}
                  >
                    ✓
                  </div>
                  <span style={{ fontSize: "13px", color: "#1A2B3C" }}>{item}</span>
                </div>
              ))}
            </div>
            <button
              type="button"
              onClick={() => onNavigate("public")}
              className="inline-flex items-center gap-2 mt-7 transition-all"
              style={{ backgroundColor: "transparent", color: "#1B6CA8", fontSize: "13px", fontWeight: 600 }}
            >
              <ArrowLeft size={14} />
              Вернуться ко входу пациента
            </button>
          </div>

          <div
            className="rounded-3xl overflow-hidden"
            style={{
              backgroundColor: "#FFFFFF",
              border: "1px solid #E8EEF4",
              boxShadow: "0 4px 24px rgba(27,108,168,0.06)",
            }}
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
                <div style={{ color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}>Корпоративный вход</div>
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
                  onChange={(event) => setStaffForm({ ...staffForm, email: event.target.value })}
                  className="w-full px-4 py-3 rounded-xl outline-none"
                  style={{
                    backgroundColor: "#F0F5FA",
                    border: "1px solid #E0EAF3",
                    fontSize: "14px",
                    color: "#1A2B3C",
                  }}
                />
              </div>
              <div className="flex flex-col gap-1.5">
                <label style={{ fontSize: "13px", fontWeight: 500, color: "#4A6480" }}>Пароль</label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    placeholder="••••••••"
                    value={staffForm.password}
                    onChange={(event) => setStaffForm({ ...staffForm, password: event.target.value })}
                    className="w-full px-4 py-3 rounded-xl outline-none pr-12"
                    style={{
                      backgroundColor: "#F0F5FA",
                      border: "1px solid #E0EAF3",
                      fontSize: "14px",
                      color: "#1A2B3C",
                    }}
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
              <button
                type="submit"
                className="w-full py-3 rounded-xl transition-all"
                style={{ backgroundColor: "#1A2B3C", color: "#FFFFFF", fontSize: "14px", fontWeight: 600 }}
              >
                Войти как сотрудник
              </button>
            </form>
          </div>
        </div>
      </section>

      <Footer onNavigate={onNavigate} />
    </div>
  );
}
