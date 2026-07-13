from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any


@dataclass
class Finding:
    """
    Единый объект результата проверки любого аудитора.

    Все аудиторы обязаны возвращать Finding или List[Finding].
    Произвольные словари и динамические структуры запрещены.
    """

    rule_id: str
    title: str
    description: str
    url: str
    severity: str  # P0, P1, P2, P3
    confidence: float  # 0.00 — 1.00
    autofix: bool
    requires_confirmation: bool
    rollback_required: bool
    framework_reference: str  # FW-001, SEO-003, OPS-004
    category: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    agent_version: str = "LAOS-1.0.0"
    # Дополнительные технические данные, специфичные для аудитора
    metadata: Dict[str, Any] = field(default_factory=dict)
    # Список возможных действий для Action Engine
    suggested_actions: List[Dict[str, Any]] = field(default_factory=list)
    # Идентификатор сессии аудита
    session_id: Optional[str] = None

    def __post_init__(self):
        self.severity = self.severity.upper()
        if self.severity not in {"P0", "P1", "P2", "P3"}:
            raise ValueError(f"severity must be P0/P1/P2/P3, got {self.severity}")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"confidence must be in [0.0, 1.0], got {self.confidence}")
        if not self.framework_reference:
            raise ValueError("framework_reference is required")
        if not self.rule_id:
            raise ValueError("rule_id is required")
        if not self.url:
            raise ValueError("url is required")
        if not self.title:
            raise ValueError("title is required")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Finding":
        return cls(**data)


@dataclass
class Decision:
    """
    Решение Decision Engine.
    """

    action: str  # autofix | ask | issue | reject | framework_improvement
    reason: str
    assigned_engine: str
    requires_rollback: bool
    owner_prompt: Optional[str] = None
    finding: Optional[Finding] = None
    log_level: str = "info"

    def __post_init__(self):
        if self.action not in {"autofix", "ask", "issue", "reject", "framework_improvement"}:
            raise ValueError(f"invalid action: {self.action}")

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "action": self.action,
            "reason": self.reason,
            "assigned_engine": self.assigned_engine,
            "requires_rollback": self.requires_rollback,
        }
        if self.owner_prompt is not None:
            data["owner_prompt"] = self.owner_prompt
        if self.log_level is not None:
            data["log_level"] = self.log_level
        if self.finding is not None:
            data["finding"] = self.finding.to_dict()
        return data
