from typing import Dict, Any, Optional
from AI.Models.finding import Finding, Decision


class DecisionEngine:
    """
    Центральный компонент принятия решений LAOS.
    """

    def __init__(self, framework_registry: Optional[Dict[str, Any]] = None):
        self.registry = framework_registry or {}
        self.version = "1.0.0"

    def decide(self, finding: Finding) -> Decision:
        # 1. Проверка Framework Reference
        if not finding.framework_reference or not self._rule_exists(finding.framework_reference):
            return Decision(
                action="framework_improvement",
                reason=f"Framework reference {finding.framework_reference} missing or unknown",
                assigned_engine="none",
                requires_rollback=False,
                owner_prompt=f"Требуется добавить правило {finding.framework_reference} для {finding.rule_id}.",
                finding=finding,
                log_level="warning"
            )

        # 2. P0 — всегда запрещён autofix
        if finding.severity == "P0":
            return Decision(
                action="issue",
                reason="P0: critical issue, autofix prohibited",
                assigned_engine="none",
                requires_rollback=False,
                owner_prompt=f"Критическая проблема: {finding.title}. Требуется немедленная проверка.",
                finding=finding,
                log_level="error"
            )

        # 3. P1 — требуется подтверждение владельца
        if finding.severity == "P1":
            return Decision(
                action="ask",
                reason="P1: high severity, owner confirmation required",
                assigned_engine="none",
                requires_rollback=finding.rollback_required,
                owner_prompt=f"Требуется подтверждение: {finding.title}. {finding.description}",
                finding=finding,
                log_level="warning"
            )

        # 4. Confidence < 0.70 — autofix запрещён
        if finding.confidence < 0.70:
            if finding.severity == "P3":
                return Decision(
                    action="reject",
                    reason="P3 + confidence < 0.70: likely false positive",
                    assigned_engine="none",
                    requires_rollback=False,
                    finding=finding,
                    log_level="info"
                )
            return Decision(
                action="issue",
                reason=f"confidence {finding.confidence} < 0.70, manual review required",
                assigned_engine="none",
                requires_rollback=False,
                finding=finding,
                log_level="warning"
            )

        # 5. P2/P3 с confidence ≥ 0.70
        if finding.severity in {"P2", "P3"}:
            if finding.autofix:
                return Decision(
                    action="autofix",
                    reason=f"{finding.severity}, confidence {finding.confidence}, autofix enabled",
                    assigned_engine="action_engine",
                    requires_rollback=finding.rollback_required,
                    finding=finding,
                    log_level="info"
                )
            return Decision(
                action="issue",
                reason=f"{finding.severity}, autofix disabled",
                assigned_engine="none",
                requires_rollback=False,
                finding=finding,
                log_level="warning"
            )

        # Fallback — не должно достигаться
        return Decision(
            action="issue",
            reason="Unhandled decision case",
            assigned_engine="none",
            requires_rollback=False,
            finding=finding,
            log_level="error"
        )

    def _rule_exists(self, reference: str) -> bool:
        # В MVP проверяем по шаблону: FW-XXX, SEO-XXX, OPS-XXX, SEC-XXX, PERF-XXX, UX-XXX
        prefixes = ("FW-", "SEO-", "OPS-", "SEC-", "PERF-", "UX-", "STRUCT-", "IMG-")
        return reference.startswith(prefixes) and len(reference) >= 4

    def set_framework_registry(self, registry: Dict[str, Any]):
        self.registry = registry
