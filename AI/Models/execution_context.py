from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import uuid


@dataclass
class ExecutionContext:
    """
    Контекст выполнения одного действия.
    Связывает Finding, Decision, Approval, Dry Run, Backup, Verification.
    """
    session_id: str
    finding_id: str
    decision: str
    approval_uuid: Optional[str] = None
    dry_run_uuid: Optional[str] = None
    backup_uuid: Optional[str] = None
    environment: str = "development"
    capability: str = ""
    owner_override: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "finding_id": self.finding_id,
            "decision": self.decision,
            "approval_uuid": self.approval_uuid,
            "dry_run_uuid": self.dry_run_uuid,
            "backup_uuid": self.backup_uuid,
            "environment": self.environment,
            "capability": self.capability,
            "owner_override": self.owner_override,
        }
