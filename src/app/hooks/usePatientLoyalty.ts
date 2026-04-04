import { useEffect, useState } from "react";

import { fetchPatientLedger, fetchPatientWallet } from "../services/loyaltyApi";
import { LoyaltyLedgerEntry, LoyaltyWallet } from "../services/loyaltyTypes";

export function usePatientLoyalty(patientId: string | null, enabled = true) {
  const [wallet, setWallet] = useState<LoyaltyWallet | null>(null);
  const [ledger, setLedger] = useState<LoyaltyLedgerEntry[]>([]);
  const [loading, setLoading] = useState(enabled);
  const [error, setError] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState(0);

  useEffect(() => {
    if (!enabled || !patientId) {
      setWallet(null);
      setLedger([]);
      setLoading(false);
      setError(null);
      return;
    }

    let isActive = true;
    setLoading(true);
    setError(null);

    Promise.all([fetchPatientWallet(patientId), fetchPatientLedger(patientId)])
      .then(([walletResponse, ledgerResponse]) => {
        if (!isActive) {
          return;
        }

        setWallet(walletResponse);
        setLedger(ledgerResponse);
      })
      .catch((requestError) => {
        if (!isActive) {
          return;
        }

        setWallet(null);
        setLedger([]);
        setError(
          requestError instanceof Error
            ? requestError.message
            : "Не удалось загрузить бонусные данные.",
        );
      })
      .finally(() => {
        if (isActive) {
          setLoading(false);
        }
      });

    return () => {
      isActive = false;
    };
  }, [patientId, enabled, refreshToken]);

  return {
    wallet,
    ledger,
    loading,
    error,
    refetch: () => setRefreshToken((currentToken) => currentToken + 1),
  };
}
