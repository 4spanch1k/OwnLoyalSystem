import { LoyaltyDirection, LoyaltyLedgerEntry } from "./loyaltyTypes";

const moneyFormatter = new Intl.NumberFormat("ru-RU", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

const dateFormatter = new Intl.DateTimeFormat("ru-RU", {
  day: "numeric",
  month: "long",
  hour: "2-digit",
  minute: "2-digit",
});

const ENTRY_TYPE_LABELS: Record<string, string> = {
  accrual: "Начисление",
  redeem: "Списание",
  rollback: "Откат",
  manual_adjustment: "Ручная корректировка",
  expire: "Сгорание",
};

const REASON_CODE_LABELS: Record<string, string> = {
  payment_confirmed: "Подтверждённая оплата",
  payment_refund_full: "Полный возврат",
  payment_refund_partial: "Частичный возврат",
  customer_support_correction: "Корректировка поддержки",
  billing_fix: "Исправление оплаты",
  migration_fix: "Исправление миграции",
  goodwill_credit: "Компенсация пациенту",
  fraud_reversal: "Аннулирование спорной операции",
  admin_error_fix: "Исправление ошибки администратора",
  redemption_apply: "Списание на приёме",
};

export const formatBonusAmount = (amount: number): string => moneyFormatter.format(amount);

export const formatLoyaltyDate = (value: string | null | undefined): string => {
  if (!value) {
    return "ещё не обновлялось";
  }

  const parsedDate = new Date(value);
  if (Number.isNaN(parsedDate.getTime())) {
    return "дата недоступна";
  }

  return dateFormatter.format(parsedDate);
};

export const getLedgerEntryTypeLabel = (entryType: string): string =>
  ENTRY_TYPE_LABELS[entryType] ?? "Операция";

export const getReasonCodeLabel = (reasonCode: string | null | undefined): string => {
  if (!reasonCode) {
    return "Операция в программе лояльности";
  }

  return REASON_CODE_LABELS[reasonCode] ?? "Операция в программе лояльности";
};

export const getDirectionPrefix = (direction: LoyaltyDirection | null): string => {
  if (direction === "credit") {
    return "+";
  }

  if (direction === "debit") {
    return "−";
  }

  return "";
};

export const getDirectionTone = (direction: LoyaltyDirection | null): string =>
  direction === "credit" ? "#22A05B" : direction === "debit" ? "#D63B3B" : "#1A2B3C";

export const describeLedgerRow = (entry: LoyaltyLedgerEntry): string =>
  `${getLedgerEntryTypeLabel(entry.entryType)} · ${getReasonCodeLabel(entry.reasonCode)}`;
