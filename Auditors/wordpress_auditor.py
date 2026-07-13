import re
import requests
from typing import List, Optional
from Auditors.base_auditor import BaseAuditor
from AI.Models.finding import Finding


class WordPressAuditor(BaseAuditor):
    """
    Проверки WordPress: наличие wp-admin, тема, плагины, версия.
    """

    name = "wordpress"
    version = "1.0.0"

    def audit(self, url: str, html: str, headers: Optional[dict] = None) -> List[Finding]:
        findings = []
        h = self._headers(headers)

        # Проверка wp-admin только для корня сайта
        if not self._is_root(url):
            return findings

        try:
            admin_url = url.rstrip('/') + '/wp-admin/'
            rr = requests.get(admin_url, headers=h, timeout=15, allow_redirects=True)
            if rr.status_code != 200:
                findings.append(Finding(
                    rule_id="WP-001",
                    title="wp-admin недоступен",
                    description=f"wp-admin возвращает HTTP {rr.status_code}.",
                    url=admin_url,
                    severity="P0",
                    confidence=0.95,
                    autofix=False,
                    requires_confirmation=True,
                    rollback_required=False,
                    framework_reference="OPS-001 §4.1",
                    category="wordpress"
                ))
        except Exception as e:
            findings.append(Finding(
                rule_id="WP-002",
                title="Ошибка доступа к wp-admin",
                description=str(e),
                url=url,
                severity="P0",
                confidence=0.90,
                autofix=False,
                requires_confirmation=True,
                rollback_required=False,
                framework_reference="OPS-001 §4.1",
                category="wordpress"
            ))

        return findings

    def _is_root(self, url: str) -> bool:
        from urllib.parse import urlparse
        path = urlparse(url).path.rstrip('/')
        return path == "" or path == "/"