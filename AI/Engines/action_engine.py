from typing import Dict, Any
from AI.Models.finding import Finding, Decision


class ActionEngine:
    """
    Выполняет одобренные автоматические исправления.
    В MVP — возвращает план действий, но не редактирует сайт самостоятельно.
    """

    def __init__(self):
        self.supported_actions = {
            "edit_title",
            "edit_description",
            "normalize_h1",
            "add_canonical",
            "add_alt",
            "remove_generator_meta",
        }

    def execute(self, finding: Finding, decision: Decision) -> Dict[str, Any]:
        if not finding.suggested_actions:
            return {
                "status": "failed",
                "reason": "no suggested actions",
                "finding": finding.rule_id
            }

        action = finding.suggested_actions[0].get("type")
        if action not in self.supported_actions:
            return {
                "status": "failed",
                "reason": f"unsupported action type: {action}",
                "finding": finding.rule_id
            }

        # В MVP Action Engine не применяет изменения к сайту,
        # а возвращает инструкцию для последующего применения.
        return {
            "status": "planned",
            "action": action,
            "url": finding.url,
            "instructions": self._generate_instructions(finding, action),
            "rollback_hint": self._rollback_hint(finding)
        }

    def _generate_instructions(self, finding: Finding, action: str) -> str:
        if action == "edit_title":
            return f"Сократить title страницы {finding.url} до 60 символов. Текущий: {finding.metadata.get('current_title', 'n/a')}"
        if action == "edit_description":
            return f"Сократить description страницы {finding.url} до 160 символов. Текущий: {finding.metadata.get('current_description', 'n/a')}"
        if action == "normalize_h1":
            return f"Оставить ровно один H1 на странице {finding.url}. Текущее количество: {finding.metadata.get('h1_count', 'n/a')}"
        if action == "add_canonical":
            return f"Добавить canonical link на страницу {finding.url}."
        if action == "add_alt":
            return f"Добавить атрибуты alt к изображениям на {finding.url}."
        if action == "remove_generator_meta":
            return f"Удалить meta generator WordPress на странице {finding.url}."
        return "Manual review required."

    def _rollback_hint(self, finding: Finding) -> str:
        if not finding.rollback_required:
            return "No rollback needed for this change."
        return "Rollback via backup plugin or database revision."
