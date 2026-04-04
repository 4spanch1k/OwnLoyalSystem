import { AlertCircle, Clock3, Gift, TrendingUp, Wallet } from "lucide-react";

import { formatBonusAmount, formatLoyaltyDate } from "../../services/loyaltyFormatting";
import { LoyaltyWallet } from "../../services/loyaltyTypes";

interface Props {
  wallet: LoyaltyWallet | null;
  loading: boolean;
  error: string | null;
}

export function PatientWalletCard({ wallet, loading, error }: Props) {
  const availableBalance = wallet?.availableBalance ?? 0;
  const lifetimeAccrued = wallet?.lifetimeAccrued ?? 0;
  const lifetimeRedeemed = wallet?.lifetimeRedeemed ?? 0;

  return (
    <div
      className="rounded-2xl p-5 relative overflow-hidden"
      style={{ background: "linear-gradient(135deg, #1B6CA8 0%, #0F4C7A 100%)" }}
    >
      <div
        className="absolute -right-8 -top-8 w-32 h-32 rounded-full opacity-10"
        style={{ backgroundColor: "#FFFFFF" }}
      />
      <div
        className="absolute -right-2 bottom-4 w-16 h-16 rounded-full opacity-5"
        style={{ backgroundColor: "#FFFFFF" }}
      />

      <div className="flex items-start justify-between mb-4 relative z-10">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Gift size={15} color="rgba(255,255,255,0.8)" />
            <span
              style={{ fontSize: "12px", color: "rgba(255,255,255,0.7)", fontWeight: 500 }}
            >
              Мои бонусы
            </span>
          </div>
          <div
            style={{ fontSize: "32px", fontWeight: 700, color: "#FFFFFF", lineHeight: 1 }}
          >
            {loading ? "—" : formatBonusAmount(availableBalance)}
          </div>
          <div
            style={{
              fontSize: "12px",
              color: "rgba(255,255,255,0.6)",
              marginTop: "2px",
            }}
          >
            {loading
              ? "Подключаем реальный бонусный баланс"
              : "доступно для следующего визита"}
          </div>
        </div>
        <div
          className="px-3 py-1.5 rounded-full flex items-center gap-1"
          style={{ backgroundColor: "rgba(255,255,255,0.15)" }}
        >
          <Wallet size={11} color="#4FC3D4" />
          <span style={{ fontSize: "11px", color: "#FFFFFF", fontWeight: 500 }}>
            {loading ? "обновляем" : "реальные данные"}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 relative z-10">
        {[
          {
            icon: TrendingUp,
            label: "Начислено всего",
            value: loading ? "—" : formatBonusAmount(lifetimeAccrued),
          },
          {
            icon: Wallet,
            label: "Списано всего",
            value: loading ? "—" : formatBonusAmount(lifetimeRedeemed),
          },
        ].map((item) => {
          const Icon = item.icon;
          return (
            <div
              key={item.label}
              className="rounded-xl p-3"
              style={{ backgroundColor: "rgba(255,255,255,0.12)" }}
            >
              <div className="flex items-center gap-2 mb-2">
                <Icon size={13} color="#FFFFFF" />
                <span style={{ fontSize: "11px", color: "rgba(255,255,255,0.72)" }}>
                  {item.label}
                </span>
              </div>
              <div style={{ fontSize: "15px", fontWeight: 600, color: "#FFFFFF" }}>
                {item.value}
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-4 relative z-10">
        {error ? (
          <div
            className="rounded-xl p-3 flex items-start gap-2.5"
            style={{ backgroundColor: "rgba(255, 240, 240, 0.15)", border: "1px solid rgba(255,255,255,0.15)" }}
          >
            <AlertCircle size={14} style={{ color: "#FFE2B5", flexShrink: 0, marginTop: "1px" }} />
            <span style={{ fontSize: "12px", color: "#FFFFFF", lineHeight: 1.5 }}>{error}</span>
          </div>
        ) : (
          <div className="flex items-center gap-2" style={{ color: "rgba(255,255,255,0.72)" }}>
            <Clock3 size={13} />
            <span style={{ fontSize: "12px" }}>
              {loading ? "Обновляем данные из backend..." : `Обновлено: ${formatLoyaltyDate(wallet?.updatedAt)}`}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
