import { loyaltyPilotConfig } from "./loyaltyConfig";
import {
  LoyaltyLedgerEntry,
  LoyaltyWallet,
  ManualAdjustmentPayload,
  ManualAdjustmentResult,
} from "./loyaltyTypes";

interface WalletResponseDto {
  patient_id: string;
  available_balance: string | number;
  lifetime_accrued: string | number;
  lifetime_redeemed: string | number;
  lifetime_expired: string | number;
  currency_code: string;
  updated_at: string | null;
}

interface LedgerEntryResponseDto {
  ledger_entry_id: string;
  entry_type: string;
  direction: "credit" | "debit" | null;
  amount: string | number;
  balance_after: string | number;
  payment_id: string | null;
  reason_code: string | null;
  currency_code: string;
  created_at: string;
  status: string;
}

interface LedgerFeedResponseDto {
  items: LedgerEntryResponseDto[];
}

interface ManualAdjustmentResponseDto {
  adjustment_id: string;
  patient_id: string;
  wallet_id: string;
  direction: "credit" | "debit";
  amount: string | number;
  balance_before: string | number;
  wallet_balance_after: string | number;
  reason_code: string;
  comment: string;
  ledger_entry_id: string;
  audit_log_id: string;
  applied_at: string;
}

type RequestOptions = {
  method?: "GET" | "POST";
  body?: unknown;
  actorUserId?: string | null;
};

class LoyaltyApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

const trimTrailingSlash = (value: string): string => value.replace(/\/$/, "");
const apiBaseUrl = `${trimTrailingSlash(loyaltyPilotConfig.apiBaseUrl)}${loyaltyPilotConfig.apiPrefix}`;

const toNumber = (value: string | number): number =>
  typeof value === "number" ? value : Number.parseFloat(value);

const buildHeaders = (actorUserId?: string | null, includeJsonContentType = false): Headers => {
  const headers = new Headers({
    "X-Tenant-Id": loyaltyPilotConfig.tenantId,
  });

  if (includeJsonContentType) {
    headers.set("Content-Type", "application/json");
  }

  if (actorUserId) {
    headers.set("X-Actor-User-Id", actorUserId);
  }

  return headers;
};

const parseErrorDetail = async (response: Response): Promise<string | null> => {
  try {
    const payload = (await response.json()) as { detail?: unknown };
    return typeof payload.detail === "string" ? payload.detail : null;
  } catch {
    return null;
  }
};

const getWalletErrorMessage = (status: number): string => {
  if (status === 404) {
    return "Пациент пока не найден в бонусной системе.";
  }

  return "Не удалось загрузить бонусный баланс.";
};

const getLedgerErrorMessage = (status: number): string => {
  if (status === 404) {
    return "История бонусов пока недоступна для этого пациента.";
  }

  return "Не удалось загрузить историю бонусов.";
};

const getManualAdjustmentErrorMessage = (status: number, detail: string | null): string => {
  if (status === 403) {
    return "У текущего пользователя нет прав на ручную корректировку.";
  }

  if (status === 409) {
    return detail?.includes("available wallet balance")
      ? "Недостаточно доступных бонусов для списания."
      : "Корректировку не удалось применить из-за текущего состояния баланса.";
  }

  if (status === 422) {
    return "Проверьте сумму, причину и комментарий.";
  }

  if (status === 404) {
    return "Пациент или кошелёк не найдены в бонусной системе.";
  }

  return "Не удалось сохранить ручную корректировку.";
};

const requestJson = async <T>(path: string, options: RequestOptions = {}): Promise<T> => {
  const includeJsonContentType = options.body !== undefined;
  const response = await fetch(`${apiBaseUrl}${path}`, {
    method: options.method ?? "GET",
    headers: buildHeaders(options.actorUserId, includeJsonContentType),
    body: includeJsonContentType ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    const detail = await parseErrorDetail(response);
    throw new LoyaltyApiError(response.status, detail ?? "request_failed");
  }

  return (await response.json()) as T;
};

export const fetchPatientWallet = async (patientId: string): Promise<LoyaltyWallet> => {
  try {
    const response = await requestJson<WalletResponseDto>(`/patients/${patientId}/wallet`);

    return {
      patientId: response.patient_id,
      availableBalance: toNumber(response.available_balance),
      lifetimeAccrued: toNumber(response.lifetime_accrued),
      lifetimeRedeemed: toNumber(response.lifetime_redeemed),
      lifetimeExpired: toNumber(response.lifetime_expired),
      currencyCode: response.currency_code,
      updatedAt: response.updated_at,
    };
  } catch (error) {
    if (error instanceof LoyaltyApiError) {
      throw new Error(getWalletErrorMessage(error.status));
    }

    throw new Error("Не удалось загрузить бонусный баланс.");
  }
};

export const fetchPatientLedger = async (patientId: string): Promise<LoyaltyLedgerEntry[]> => {
  try {
    const response = await requestJson<LedgerFeedResponseDto>(`/patients/${patientId}/ledger`);

    return response.items.map((entry) => ({
      ledgerEntryId: entry.ledger_entry_id,
      entryType: entry.entry_type,
      direction: entry.direction,
      amount: toNumber(entry.amount),
      balanceAfter: toNumber(entry.balance_after),
      paymentId: entry.payment_id,
      reasonCode: entry.reason_code,
      currencyCode: entry.currency_code,
      createdAt: entry.created_at,
      status: entry.status,
    }));
  } catch (error) {
    if (error instanceof LoyaltyApiError) {
      throw new Error(getLedgerErrorMessage(error.status));
    }

    throw new Error("Не удалось загрузить историю бонусов.");
  }
};

export const createManualAdjustment = async (
  patientId: string,
  payload: ManualAdjustmentPayload,
): Promise<ManualAdjustmentResult> => {
  const response = await fetch(`${apiBaseUrl}/patients/${patientId}/wallet/adjustments`, {
    method: "POST",
    headers: buildHeaders(loyaltyPilotConfig.actorUserId, true),
    body: JSON.stringify({
      amount: payload.amount,
      direction: payload.direction,
      reason_code: payload.reasonCode,
      comment: payload.comment,
    }),
  });

  if (!response.ok) {
    const detail = await parseErrorDetail(response);
    throw new Error(getManualAdjustmentErrorMessage(response.status, detail));
  }

  const result = (await response.json()) as ManualAdjustmentResponseDto;

  return {
    adjustmentId: result.adjustment_id,
    patientId: result.patient_id,
    walletId: result.wallet_id,
    direction: result.direction,
    amount: toNumber(result.amount),
    balanceBefore: toNumber(result.balance_before),
    walletBalanceAfter: toNumber(result.wallet_balance_after),
    reasonCode: result.reason_code,
    comment: result.comment,
    ledgerEntryId: result.ledger_entry_id,
    auditLogId: result.audit_log_id,
    appliedAt: result.applied_at,
  };
};
