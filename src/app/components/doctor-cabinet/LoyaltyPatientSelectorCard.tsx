import { UserRound } from "lucide-react";

import { LoyaltyPatientOption } from "../../services/loyaltyTypes";

interface Props {
  patients: LoyaltyPatientOption[];
  selectedPatientId: string | null;
  onSelect: (patientId: string) => void;
}

export function LoyaltyPatientSelectorCard({ patients, selectedPatientId, onSelect }: Props) {
  return (
    <div className="rounded-2xl p-5" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E8EEF4" }}>
      <div className="flex items-center gap-2 mb-4">
        <UserRound size={16} style={{ color: "#1B6CA8" }} />
        <span style={{ fontWeight: 600, fontSize: "15px", color: "#1A2B3C" }}>Пациент для loyalty-операций</span>
      </div>

      <div style={{ fontSize: "12px", color: "#6B8FA8", marginBottom: "12px", lineHeight: 1.5 }}>
        Для пилота используем заранее настроенные patient id. Действия всё равно валидируются backend по tenant и роли.
      </div>

      <div className="flex flex-wrap gap-2">
        {patients.map((patient) => {
          const isActive = patient.id === selectedPatientId;
          return (
            <button
              key={patient.id}
              onClick={() => onSelect(patient.id)}
              className="px-4 py-2.5 rounded-xl text-left transition-all"
              style={{
                backgroundColor: isActive ? "#EBF4FB" : "#F7F9FC",
                border: `1px solid ${isActive ? "#1B6CA8" : "#E8EEF4"}`,
              }}
            >
              <div style={{ fontSize: "13px", fontWeight: 600, color: isActive ? "#1B6CA8" : "#1A2B3C" }}>
                {patient.label}
              </div>
              <div style={{ fontSize: "11px", color: "#6B8FA8", marginTop: "3px" }}>{patient.id}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
