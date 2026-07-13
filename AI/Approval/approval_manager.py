from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
import uuid


@dataclass
class ApprovalRequest:
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    reason: str = ""
    risks: List[str] = field(default_factory=list)
    rollback_plan: Dict[str, Any] = field(default_factory=dict)
    target_url: str = ""
    proposed_changes: List[Dict[str, Any]] = field(default_factory=list)
    requested_by: str = "agent"
    requested_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "waiting"  # waiting | approved | rejected | expired
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    expires_at: str = field(default_factory=lambda: (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat())
    dry_run_uuid: Optional[str] = None
    finding_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def approve(self, owner: str):
        self.status = "approved"
        self.approved_by = owner
        self.approved_at = datetime.now(timezone.utc).isoformat()

    def reject(self, owner: str):
        self.status = "rejected"
        self.approved_by = owner
        self.approved_at = datetime.now(timezone.utc).isoformat()

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > datetime.fromisoformat(self.expires_at)


class ApprovalManager:
    """
    Хранит и управляет approval requests.
    """

    def __init__(self):
        self.requests: Dict[str, ApprovalRequest] = {}

    def create(self, finding, decision, dry_run: Optional[Dict[str, Any]] = None) -> ApprovalRequest:
        req = ApprovalRequest(
            title=finding.title,
            description=finding.description,
            reason=decision.reason,
            risks=["potential_side_effects", "seo_fluctuation"],
            rollback_plan=dry_run.get("rollback_plan", {}) if dry_run else {},
            target_url=finding.url,
            proposed_changes=dry_run.get("proposed_changes", []) if dry_run else [],
            dry_run_uuid=dry_run.get("dry_run_uuid") if dry_run else None,
            finding_id=finding.rule_id,
        )
        self.requests[req.uuid] = req
        return req

    def get(self, approval_uuid: str) -> Optional[ApprovalRequest]:
        req = self.requests.get(approval_uuid)
        if req and req.status == "waiting" and req.is_expired():
            req.status = "expired"
        return req

    def approve(self, approval_uuid: str, owner: str) -> Optional[ApprovalRequest]:
        req = self.get(approval_uuid)
        if not req or req.status != "waiting":
            return None
        req.approve(owner)
        return req

    def reject(self, approval_uuid: str, owner: str) -> Optional[ApprovalRequest]:
        req = self.get(approval_uuid)
        if not req or req.status != "waiting":
            return None
        req.reject(owner)
        return req

    def list_waiting(self) -> List[ApprovalRequest]:
        return [r for r in self.requests.values() if r.status == "waiting"]
