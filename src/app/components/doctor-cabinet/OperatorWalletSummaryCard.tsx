import { AlertCircle, Clock3, Gift, TrendingUp, Wallet } from "lucide-react";

import { formatBonusAmount, formatLoyaltyDate } from "../../services/loyaltyFormatting";
import { LoyaltyWallet } from "../../services/loyaltyTypes";

interface Props {
  patientLabel: string;
  wallet: LoyaltyWallet | null;
  loading: boolean;
  error: string | null;
}

export function OperatorWalletSummaryCard({ patientLabel, wallet, loading, error }: Props) {
  return (
    <div className="rounded-2xl p-5" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
      <div className="flex items-center gap-2 mb-4">
        <Gift size={16} style={{ color: "#1B6CA8" }} />
        <span style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>Баланс пациента</span>
      </div>

      <div className="rounded-xl p-4 mb-4" style={{ backgroundColor: "#F0F5FA" }}>
        <div style={{ fontSize: "12px", color: "#6B8FA8" }}>{patientLabel}</div>
        <div style={{ fontSize: "26px", fontWeight: 700, color: "#1A2B3C", marginTop: "8px" }}>
          {loading ? "—" : formatBonusAmount(wallet?.availableBalance ?? 0)}
        </div>
        <div style={{ fontSize: "12px", color: "#6B8FA8", marginTop: "6px" }}>
          {loading
            ? "Подключаем баланс из backend"
            : `Доступно сейчас для loyalty-операций`}
        </div>
      </div>

      {error ? (
        <div
          className="rounded-xl p-3 flex items-start gap-2.5 mb-4"
          style={{ backgroundColor: "#FFF8EC", border: "1px solid #FCDEA3" }}
        >
          <AlertCircle size={14} style={{ color: "#E8970A", flexShrink: 0, marginTop: "1px" }} />
          <span style={{ fontSize: "12px", color: "#8A5A00", lineHeight: 1.5 }}>{error}</span>
        </div>
      ) : (
        <div className="flex items-center gap-2 mb-4" style={{ color: "#6B8FA8" }}>
          <Clock3 size={13} />
          <span style={{ fontSize: "12px" }}>
            {loading ? "Обновляем..." : `Обновлено: ${formatLoyaltyDate(wallet?.updatedAt)}`}
          </span>
        </div>
      )}

      <div className="grid grid-cols-2 gap-3">
        {[
          {
            icon: TrendingUp,
            label: "Начислено",
            value: loading ? "—" : formatBonusAmount(wallet?.lifetimeAccrued ?? 0),
          },
          {
            icon: Wallet,
            label: "Списано",
            value: loading ? "—" : formatBonusAmount(wallet?.lifetimeRedeemed ?? 0),
          },
        ].map((metric) => {
          const Icon = metric.icon;
          return (
            <div
              key={metric.label}
              className="rounded-xl p-3"
              style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4" }}
            >
              <div className="flex items-center gap-2 mb-2">
                <Icon size={13} style={{ color: "#1B6CA8" }} />
                <span style={{ fontSize: "11px", color: "#6B8FA8" }}>{metric.label}</span>
              </div>
              <div style={{ fontSize: "14px", fontWeight: 600, color: "#1A2B3C" }}>{metric.value}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
