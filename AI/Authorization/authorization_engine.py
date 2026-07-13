from typing import Dict, Any, Optional
from AI.Models.finding import Finding, Decision


class AuthorizationEngine:
    """
    Отвечает только на один вопрос: Можно ли выполнить действие?
    """

    def __init__(
        self,
        environment_config: Dict[str, Any],
        capabilities_config: Dict[str, Any],
        approvals: Optional[Dict[str, Any]] = None,
    ):
        self.environment = environment_config
        self.capabilities = capabilities_config
        self.approvals = approvals or {}

    def authorize(self, finding: Finding, decision: Decision, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        checks = []

        # 1. Environment exists and not locked
        env_name = self.environment.get("name")
        if not env_name:
            checks.append({"check": "environment_exists", "passed": False, "reason": "No environment configured"})
        else:
            checks.append({"check": "environment_exists", "passed": True, "value": env_name})

        production_lock = self.environment.get("production_lock", False)
        if production_lock and env_name == "production":
            checks.append({"check": "production_lock", "passed": False, "reason": "Production lock is active"})
        else:
            checks.append({"check": "production_lock", "passed": True})

        # 2. Capability exists
        category = finding.category
        capability = self.capabilities.get(category, {})
        if not capability.get("enabled", False):
            checks.append({"check": "capability_enabled", "passed": False, "reason": f"Capability {category} disabled"})
        else:
            checks.append({"check": "capability_enabled", "passed": True, "value": category})

        # 3. Severity rules
        if finding.severity in ("P0", "P1"):
            checks.append({"check": "severity", "passed": False, "reason": f"Severity {finding.severity} requires owner approval"})
        else:
            checks.append({"check": "severity", "passed": True, "value": finding.severity})

        # 4. Confidence threshold
        if finding.confidence < 0.70:
            checks.append({"check": "confidence", "passed": False, "reason": f"Confidence {finding.confidence} below 0.70"})
        else:
            checks.append({"check": "confidence", "passed": True, "value": finding.confidence})

        # 5. Approval if required
        approval_uuid = context.get("approval_uuid")
        if decision.action == "autofix" and (finding.severity in ("P0", "P1") or self.environment.get("name") == "production"):
            if not approval_uuid or approval_uuid not in self.approvals:
                checks.append({"check": "approval", "passed": False, "reason": "Required approval missing"})
            else:
                approval = self.approvals[approval_uuid]
                if approval.get("status") != "approved":
                    checks.append({"check": "approval", "passed": False, "reason": f"Approval status: {approval.get('status')}"})
                else:
                    checks.append({"check": "approval", "passed": True, "value": approval_uuid})
        else:
            checks.append({"check": "approval", "passed": True, "reason": "Not required"})

        # 6. Backup present
        backup_uuid = context.get("backup_uuid")
        if finding.rollback_required and not backup_uuid:
            checks.append({"check": "backup", "passed": False, "reason": "Rollback required but backup missing"})
        else:
            checks.append({"check": "backup", "passed": True, "value": backup_uuid})

        # 7. Dry run present
        dry_run_uuid = context.get("dry_run_uuid")
        if decision.action == "autofix" and not dry_run_uuid:
            checks.append({"check": "dry_run", "passed": False, "reason": "Dry Run required for autofix"})
        else:
            checks.append({"check": "dry_run", "passed": True, "value": dry_run_uuid})

        # 8. Framework reference
        if not finding.framework_reference:
            checks.append({"check": "framework_reference", "passed": False, "reason": "Missing framework reference"})
        else:
            checks.append({"check": "framework_reference", "passed": True, "value": finding.framework_reference})

        failed = [c for c in checks if not c["passed"]]
        allowed = len(failed) == 0

        return {
            "allowed": allowed,
            "reason": failed[0]["reason"] if failed else "authorized",
            "checks": checks,
            "environment": env_name,
            "capability": category,
        }
