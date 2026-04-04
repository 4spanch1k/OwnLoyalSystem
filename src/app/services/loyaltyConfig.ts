import { LoyaltyPatientOption } from "./loyaltyTypes";

const normalizeEnvValue = (value: string | undefined): string | null => {
  const trimmedValue = value?.trim();
  return trimmedValue ? trimmedValue : null;
};

const apiBaseUrl = normalizeEnvValue(import.meta.env.VITE_LOYALTY_API_BASE_URL) ?? "";
const tenantId = normalizeEnvValue(import.meta.env.VITE_LOYALTY_TENANT_ID) ?? "tenant-manual-adjustment";
const dashboardPatientId =
  normalizeEnvValue(import.meta.env.VITE_LOYALTY_PATIENT_ID) ?? "patient-manual-adjustment";
const actorUserId =
  normalizeEnvValue(import.meta.env.VITE_LOYALTY_ACTOR_USER_ID) ?? "user-clinic-manager";
const extraOperatorPatientId = normalizeEnvValue(import.meta.env.VITE_LOYALTY_OPERATOR_PATIENT_ID);
const extraOperatorPatientLabel =
  normalizeEnvValue(import.meta.env.VITE_LOYALTY_OPERATOR_PATIENT_LABEL) ?? "Пациент из интеграции";

const operatorPatients: LoyaltyPatientOption[] = [
  { id: dashboardPatientId, label: "Анна Сергеевна Кузнецова" },
  ...(extraOperatorPatientId && extraOperatorPatientId !== dashboardPatientId
    ? [{ id: extraOperatorPatientId, label: extraOperatorPatientLabel }]
    : []),
];

export const loyaltyPilotConfig = {
  apiBaseUrl,
  apiPrefix: "/api/v1",
  tenantId,
  dashboardPatientId,
  actorUserId,
  operatorPatients,
};

export const manualAdjustmentReasonOptions = [
  { value: "customer_support_correction", label: "Корректировка поддержки" },
  { value: "billing_fix", label: "Исправление оплаты" },
  { value: "migration_fix", label: "Исправление миграции" },
  { value: "goodwill_credit", label: "Компенсация пациенту" },
  { value: "fraud_reversal", label: "Аннулирование спорной операции" },
  { value: "admin_error_fix", label: "Исправление ошибки администратора" },
];
