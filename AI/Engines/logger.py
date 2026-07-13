import os
import json
from datetime import datetime, timezone
from typing import Dict, Any


class Logger:
    """
    Унифицированное логирование всех этапов.
    """

    def __init__(self, log_dir: str = "/root/laser178-ai-framework/Logs"):
        self.log_dir = log_dir
        self.session_id = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
        os.makedirs(os.path.join(self.log_dir, self.session_id), exist_ok=True)

    def _write(self, step: str, data: Dict[str, Any]):
        path = os.path.join(self.log_dir, self.session_id, f"{step}.jsonl")
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

    def log_audit(self, findings: list):
        self._write("audit", {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "count": len(findings),
            "findings": [f.to_dict() for f in findings]
        })

    def log_event(self, event_type: str, data: Dict[str, Any]):
        self._write(event_type, data)

    def log_decision(self, finding_id: str, decision: Any):
        from AI.Models.finding import Decision, Finding
        data = decision.__dict__
        if isinstance(decision, Decision):
            data = decision.to_dict()
        self._write("decision", {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "finding_id": finding_id,
            "decision": data
        })

    def log_action(self, finding_id: str, result: Dict[str, Any]):
        self._write("action", {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "finding_id": finding_id,
            "result": result
        })

    def log_verification(self, finding_id: str, result: Dict[str, Any]):
        self._write("verification", {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "finding_id": finding_id,
            "result": result
        })

    def log_issue(self, finding_id: str, issue_number: int, reason: str):
        self._write("issue", {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "finding_id": finding_id,
            "issue_number": issue_number,
            "reason": reason
        })
