import { AlertCircle, Clock3, History, RefreshCcw, TrendingUp, Wallet } from "lucide-react";

import {
  describeLedgerRow,
  formatBonusAmount,
  formatLoyaltyDate,
  getDirectionPrefix,
  getDirectionTone,
} from "../../services/loyaltyFormatting";
import { LoyaltyLedgerEntry } from "../../services/loyaltyTypes";

interface Props {
  title: string;
  entries: LoyaltyLedgerEntry[];
  loading: boolean;
  error: string | null;
  emptyTitle: string;
  emptyDescription: string;
}

const ENTRY_ICONS = {
  credit: TrendingUp,
  debit: Wallet,
  fallback: RefreshCcw,
};

export function LoyaltyLedgerCard({
  title,
  entries,
  loading,
  error,
  emptyTitle,
  emptyDescription,
}: Props) {
  const visibleEntries = entries.slice(0, 5);

  return (
    <div className="rounded-2xl p-5" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
      <div className="flex items-center gap-2 mb-4">
        <History size={16} style={{ color: "#1B6CA8" }} />
        <span style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>{title}</span>
      </div>

      {loading ? (
        <div className="flex flex-col gap-3">
          {[1, 2, 3].map((item) => (
            <div
              key={item}
              className="rounded-xl p-4"
              style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4" }}
            >
              <div
                className="h-3 rounded-full mb-3"
                style={{ width: `${55 + item * 10}%`, backgroundColor: "#E8EEF4" }}
              />
              <div className="h-2.5 rounded-full" style={{ width: "40%", backgroundColor: "#E8EEF4" }} />
            </div>
          ))}
        </div>
      ) : error ? (
        <div
          className="rounded-xl p-4 flex items-start gap-3"
          style={{ backgroundColor: "#FFF8EC", border: "1px solid #FCDEA3" }}
        >
          <AlertCircle size={15} style={{ color: "#E8970A", marginTop: "1px", flexShrink: 0 }} />
          <div>
            <div style={{ fontSize: "13px", fontWeight: 600, color: "#8A5A00" }}>
              Не удалось загрузить историю
            </div>
            <div style={{ fontSize: "12px", color: "#A07030", marginTop: "4px", lineHeight: 1.5 }}>
              {error}
            </div>
          </div>
        </div>
      ) : visibleEntries.length === 0 ? (
        <div
          className="rounded-xl p-5 text-center"
          style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4" }}
        >
          <History size={28} className="mx-auto mb-3" style={{ color: "#D0E6F5" }} />
          <div style={{ fontSize: "14px", fontWeight: 600, color: "#1A2B3C" }}>{emptyTitle}</div>
          <div style={{ fontSize: "12px", color: "#6B8FA8", marginTop: "6px", lineHeight: 1.5 }}>
            {emptyDescription}
          </div>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {visibleEntries.map((entry) => {
            const Icon =
              entry.direction === "credit"
                ? ENTRY_ICONS.credit
                : entry.direction === "debit"
                  ? ENTRY_ICONS.debit
                  : ENTRY_ICONS.fallback;

            return (
              <div
                key={entry.ledgerEntryId}
                className="rounded-xl p-4"
                style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4" }}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <div
                        className="w-9 h-9 rounded-xl flex items-center justify-center shrink-0"
                        style={{ backgroundColor: "#EBF4FB", color: "#1B6CA8" }}
                      >
                        <Icon size={15} />
                      </div>
                      <div className="min-w-0">
                        <div
                          style={{
                            fontSize: "13px",
                            fontWeight: 600,
                            color: "#1A2B3C",
                            lineHeight: 1.4,
                          }}
                        >
                          {describeLedgerRow(entry)}
                        </div>
                        <div
                          className="flex items-center gap-1.5 mt-1"
                          style={{ fontSize: "11px", color: "#6B8FA8" }}
                        >
                          <Clock3 size={11} />
                          {formatLoyaltyDate(entry.createdAt)}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="text-right shrink-0">
                    <div
                      style={{
                        fontSize: "14px",
                        fontWeight: 700,
                        color: getDirectionTone(entry.direction),
                      }}
                    >
                      {getDirectionPrefix(entry.direction)}
                      {formatBonusAmount(entry.amount)}
                    </div>
                    <div style={{ fontSize: "11px", color: "#6B8FA8", marginTop: "4px" }}>
                      После операции: {formatBonusAmount(entry.balanceAfter)}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
