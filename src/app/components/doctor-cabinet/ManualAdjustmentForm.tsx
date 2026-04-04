import { useState } from "react";
import { AlertCircle, PencilLine, ShieldCheck } from "lucide-react";

import { manualAdjustmentReasonOptions } from "../../services/loyaltyConfig";
import { LoyaltyDirection, ManualAdjustmentPayload } from "../../services/loyaltyTypes";

interface Props {
  patientLabel: string;
  disabled: boolean;
  submitting: boolean;
  successMessage: string | null;
  errorMessage: string | null;
  onSubmit: (payload: ManualAdjustmentPayload) => Promise<boolean>;
}

export function ManualAdjustmentForm({
  patientLabel,
  disabled,
  submitting,
  successMessage,
  errorMessage,
  onSubmit,
}: Props) {
  const [direction, setDirection] = useState<LoyaltyDirection>("credit");
  const [amount, setAmount] = useState("");
  const [reasonCode, setReasonCode] = useState(manualAdjustmentReasonOptions[0].value);
  const [comment, setComment] = useState("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const wasSuccessful = await onSubmit({
      amount,
      direction,
      reasonCode,
      comment,
    });

    if (wasSuccessful) {
      setDirection("credit");
      setAmount("");
      setReasonCode(manualAdjustmentReasonOptions[0].value);
      setComment("");
    }
  };

  return (
    <div className="rounded-2xl p-5" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
      <div className="flex items-center gap-2 mb-4">
        <PencilLine size={16} style={{ color: "#1B6CA8" }} />
        <span style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>Ручная корректировка</span>
      </div>

      <div
        className="rounded-xl p-3 mb-4 flex items-start gap-2.5"
        style={{ backgroundColor: "#EBF4FB", border: "1px solid #D5E9F7" }}
      >
        <ShieldCheck size={14} style={{ color: "#1B6CA8", flexShrink: 0, marginTop: "1px" }} />
        <div>
          <div style={{ fontSize: "12px", fontWeight: 600, color: "#1B6CA8" }}>{patientLabel}</div>
          <div style={{ fontSize: "12px", color: "#4A6480", marginTop: "3px", lineHeight: 1.5 }}>
            После сохранения мы заново загружаем баланс и историю из backend. Без optimistic update.
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <div style={{ fontSize: "12px", color: "#6B8FA8", marginBottom: "8px", fontWeight: 500 }}>
            Направление
          </div>
          <div className="grid grid-cols-2 gap-2">
            {[
              { value: "credit" as const, label: "Добавить бонусы" },
              { value: "debit" as const, label: "Списать бонусы" },
            ].map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => setDirection(option.value)}
                className="py-3 px-3 rounded-xl transition-all"
                style={{
                  backgroundColor: direction === option.value ? "#EBF4FB" : "#F7F9FC",
                  color: direction === option.value ? "#1B6CA8" : "#4A6480",
                  border: `1px solid ${direction === option.value ? "#1B6CA8" : "#E8EEF4"}`,
                  fontSize: "13px",
                  fontWeight: direction === option.value ? 600 : 400,
                }}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>

        <div>
          <div style={{ fontSize: "12px", color: "#6B8FA8", marginBottom: "8px", fontWeight: 500 }}>
            Сумма
          </div>
          <input
            value={amount}
            onChange={(event) => setAmount(event.target.value)}
            inputMode="decimal"
            placeholder="Например, 500.00"
            className="w-full px-4 py-3 rounded-xl outline-none"
            style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4", fontSize: "13px", color: "#1A2B3C" }}
          />
        </div>

        <div>
          <div style={{ fontSize: "12px", color: "#6B8FA8", marginBottom: "8px", fontWeight: 500 }}>
            Причина
          </div>
          <select
            value={reasonCode}
            onChange={(event) => setReasonCode(event.target.value)}
            className="w-full px-4 py-3 rounded-xl outline-none"
            style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4", fontSize: "13px", color: "#1A2B3C" }}
          >
            {manualAdjustmentReasonOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <div style={{ fontSize: "12px", color: "#6B8FA8", marginBottom: "8px", fontWeight: 500 }}>
            Комментарий
          </div>
          <textarea
            value={comment}
            onChange={(event) => setComment(event.target.value)}
            rows={4}
            placeholder="Коротко объясните, почему нужна корректировка..."
            className="w-full px-4 py-3 rounded-xl outline-none resize-none"
            style={{ backgroundColor: "#F7F9FC", border: "1px solid #E8EEF4", fontSize: "13px", color: "#1A2B3C" }}
          />
        </div>

        {(successMessage || errorMessage) && (
          <div
            className="rounded-xl p-3 flex items-start gap-2.5"
            style={{
              backgroundColor: successMessage ? "#E6F5ED" : "#FFF8EC",
              border: `1px solid ${successMessage ? "#BFE4CB" : "#FCDEA3"}`,
            }}
          >
            <AlertCircle
              size={14}
              style={{
                color: successMessage ? "#22A05B" : "#E8970A",
                flexShrink: 0,
                marginTop: "1px",
              }}
            />
            <span
              style={{
                fontSize: "12px",
                color: successMessage ? "#1C6C3B" : "#8A5A00",
                lineHeight: 1.5,
              }}
            >
              {successMessage ?? errorMessage}
            </span>
          </div>
        )}

        <button
          type="submit"
          disabled={disabled || submitting}
          className="w-full py-3 rounded-xl transition-all"
          style={{
            backgroundColor: disabled || submitting ? "#D0E6F5" : "#1B6CA8",
            color: "#FFFFFF",
            fontSize: "14px",
            fontWeight: 600,
            cursor: disabled || submitting ? "not-allowed" : "pointer",
          }}
        >
          {submitting ? "Сохраняем..." : "Применить корректировку"}
        </button>
      </form>
    </div>
  );
}
