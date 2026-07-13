import importlib
import pkgutil
from typing import List, Dict, Any, Optional
import requests
from Auditors.base_auditor import BaseAuditor
from AI.Models.finding import Finding


class AuditRunner:
    """
    Оркестратор аудиторов.
    Загружает все аудиторы из папки Auditors/ и запускает их.
    """

    def __init__(self, headers: Optional[Dict[str, str]] = None):
        self.headers = headers or {"Cookie": "beget=begetok"}
        self.auditors: List[BaseAuditor] = []
        self._load_auditors()

    def _load_auditors(self):
        import Auditors
        for _, modname, ispkg in pkgutil.iter_modules(Auditors.__path__):
            if ispkg or modname in ("base_auditor",):
                continue
            try:
                module = importlib.import_module(f"Auditors.{modname}")
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, BaseAuditor) and attr is not BaseAuditor:
                        self.auditors.append(attr())
            except Exception as e:
                print(f"Failed to load auditor {modname}: {e}")

    def run_page(self, url: str) -> List[Finding]:
        r = requests.get(url, headers=self.headers, timeout=30)
        r.raise_for_status()
        html = r.text
        findings = []
        for auditor in self.auditors:
            try:
                findings.extend(auditor.audit(url, html, self.headers))
            except Exception as e:
                findings.append(Finding(
                    rule_id="FRAMEWORK-001",
                    title=f"Auditor {auditor.name} failed",
                    description=str(e),
                    url=url,
                    severity="P1",
                    confidence=0.90,
                    autofix=False,
                    requires_confirmation=True,
                    rollback_required=False,
                    framework_reference="OPS-001 §9.1",
                    category="framework"
                ))
        return findings

    def run_pages(self, urls: List[str]) -> Dict[str, List[Finding]]:
        results = {}
        for url in urls:
            results[url] = self.run_page(url)
        return results
