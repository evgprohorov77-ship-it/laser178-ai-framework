from typing import Dict, Any
from AI.Models.finding import Finding, Decision


class RiskEngine:
    """
    Оценивает риск автоматического исправления.
    """

    def __init__(self):
        self.risk_matrix = {
            "P0": 1.0,
            "P1": 0.8,
            "P2": 0.4,
            "P3": 0.1,
        }

    def assess(self, finding: Finding, decision: Decision) -> Dict[str, Any]:
        base_risk = self.risk_matrix.get(finding.severity, 0.5)
        # confidence снижает риск
        confidence_discount = 1.0 - finding.confidence
        # rollback снижает риск
        rollback_discount = 0.3 if finding.rollback_required else 0.0
        # autofix требует действия
        action_risk = 0.2 if finding.autofix else 0.0

        final_risk = min(1.0, base_risk + confidence_discount * 0.2 + action_risk - rollback_discount)

        return {
            "base_risk": base_risk,
            "final_risk": round(final_risk, 2),
            "confidence": finding.confidence,
            "severity": finding.severity,
            "rollback_available": finding.rollback_required,
            "recommendation": self._recommend(final_risk, decision)
        }

    def _recommend(self, risk: float, decision: Decision) -> str:
        if risk >= 0.8:
            return "Do not proceed automatically. Escalate to owner."
        if risk >= 0.5:
            return "Proceed with caution and verification."
        if decision.action == "autofix":
            return "Safe to proceed with autofix and verification."
        return "No automatic action required."
