import uuid
from typing import Dict, Any, List
from AI.Models.finding import Finding


class DryRunEngine:
    """
    Имитирует изменение без реального применения.
    """

    def __init__(self):
        pass

    def run(self, finding: Finding) -> Dict[str, Any]:
        proposed_changes = self._build_changes(finding)
        affected_pages = [finding.url]
        affected_files = self._guess_files(finding)
        risks = self._assess_risks(finding)
        rollback = self._rollback_plan(finding)

        return {
            "dry_run_uuid": str(uuid.uuid4()),
            "finding_id": finding.rule_id,
            "target_url": finding.url,
            "proposed_changes": proposed_changes,
            "affected_pages": affected_pages,
            "affected_files": affected_files,
            "risks": risks,
            "rollback_plan": rollback,
            "status": "ready_for_review",
        }

    def _build_changes(self, finding: Finding) -> List[Dict[str, Any]]:
        changes = []
        actions = finding.suggested_actions or []
        for action in actions:
            atype = action.get("type")
            if atype == "edit_title":
                changes.append({"field": "title", "current": finding.metadata.get("title", ""), "proposed": "[truncated to 60 chars]"})
            elif atype == "edit_description":
                changes.append({"field": "description", "current": finding.metadata.get("description", ""), "proposed": "[truncated to 160 chars]"})
            elif atype == "normalize_h1":
                changes.append({"field": "h1", "current": f"{finding.metadata.get('h1_count', 0)} H1", "proposed": "1 H1"})
            elif atype == "add_canonical":
                changes.append({"field": "canonical", "current": "missing", "proposed": finding.url})
            elif atype == "add_alt":
                changes.append({"field": "img[alt]", "current": "empty", "proposed": "descriptive alt text"})
            elif atype == "remove_generator_meta":
                changes.append({"field": "meta[generator]", "current": "WordPress x.x", "proposed": "removed"})
        return changes

    def _guess_files(self, finding: Finding) -> List[str]:
        files = []
        if finding.category == "wordpress":
            files.append("wp-content/themes/.../functions.php")
        elif finding.category == "seo":
            files.append("WordPress post/page record in wp_posts")
        return files

    def _assess_risks(self, finding: Finding) -> List[Dict[str, Any]]:
        return [
            {"risk": "layout_shift", "probability": 0.1, "impact": "low"},
            {"risk": "seo_fluctuation", "probability": 0.2, "impact": "low"},
        ]

    def _rollback_plan(self, finding: Finding) -> Dict[str, Any]:
        return {
            "method": "restore_from_backup",
            "estimated_time": "2 minutes",
            "automation_ready": True,
        }
