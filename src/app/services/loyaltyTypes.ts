export type LoyaltyDirection = "credit" | "debit";

export interface LoyaltyWallet {
  patientId: string;
  availableBalance: number;
  lifetimeAccrued: number;
  lifetimeRedeemed: number;
  lifetimeExpired: number;
  currencyCode: string;
  updatedAt: string | null;
}

export interface LoyaltyLedgerEntry {
  ledgerEntryId: string;
  entryType: string;
  direction: LoyaltyDirection | null;
  amount: number;
  balanceAfter: number;
  paymentId: string | null;
  reasonCode: string | null;
  currencyCode: string;
  createdAt: string;
  status: string;
}

export interface ManualAdjustmentPayload {
  amount: string;
  direction: LoyaltyDirection;
  reasonCode: string;
  comment: string;
}

export interface ManualAdjustmentResult {
  adjustmentId: string;
  patientId: string;
  walletId: string;
  direction: LoyaltyDirection;
  amount: number;
  balanceBefore: number;
  walletBalanceAfter: number;
  reasonCode: string;
  comment: string;
  ledgerEntryId: string;
  auditLogId: string;
  appliedAt: string;
}

export interface LoyaltyPatientOption {
  id: string;
  label: string;
}
