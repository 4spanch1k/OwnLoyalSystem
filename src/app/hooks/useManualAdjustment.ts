import { useCallback, useState } from "react";

import { createManualAdjustment } from "../services/loyaltyApi";
import { ManualAdjustmentPayload } from "../services/loyaltyTypes";

export function useManualAdjustment(patientId: string | null, onSuccess: () => void) {
  const [submitting, setSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const submitAdjustment = async (payload: ManualAdjustmentPayload): Promise<boolean> => {
    if (!patientId) {
      setSuccessMessage(null);
      setErrorMessage("Сначала выберите пациента для корректировки.");
      return false;
    }

    const normalizedAmount = Number.parseFloat(payload.amount.replace(",", "."));
    if (!Number.isFinite(normalizedAmount) || normalizedAmount <= 0) {
      setSuccessMessage(null);
      setErrorMessage("Введите корректную сумму больше нуля.");
      return false;
    }

    if (!payload.reasonCode.trim()) {
      setSuccessMessage(null);
      setErrorMessage("Выберите причину корректировки.");
      return false;
    }

    if (payload.comment.trim().length < 5) {
      setSuccessMessage(null);
      setErrorMessage("Комментарий должен быть понятным и не короче 5 символов.");
      return false;
    }

    setSubmitting(true);
    setSuccessMessage(null);
    setErrorMessage(null);

    try {
      await createManualAdjustment(patientId, payload);
      setSuccessMessage("Корректировка сохранена. История и баланс обновлены.");
      onSuccess();
      return true;
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Не удалось сохранить ручную корректировку.",
      );
      return false;
    } finally {
      setSubmitting(false);
    }
  };

  return {
    submitting,
    successMessage,
    errorMessage,
    submitAdjustment,
    clearFeedback: useCallback(() => {
      setSuccessMessage(null);
      setErrorMessage(null);
    }, []),
  };
}
