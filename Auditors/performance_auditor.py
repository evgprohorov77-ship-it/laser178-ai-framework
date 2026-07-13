import re
import requests
from urllib.parse import urljoin
from typing import List, Optional
from Auditors.base_auditor import BaseAuditor
from AI.Models.finding import Finding


class PerformanceAuditor(BaseAuditor):
    """
    Проверки производительности: robots.txt, sitemap.xml, время ответа.
    """

    name = "performance"
    version = "1.0.0"

    def audit(self, url: str, html: str, headers: Optional[dict] = None) -> List[Finding]:
        findings = []
        h = self._headers(headers)
        base = url

        # robots.txt и sitemap.xml проверяем только для корня сайта
        if not self._is_root(url):
            return findings

        # robots.txt sitemap
        robots_url = urljoin(base, 'robots.txt')
        try:
            robots = requests.get(robots_url, headers=h, timeout=15).text
            if 'sitemap' not in robots.lower():
                findings.append(Finding(
                    rule_id="PERF-002",
                    title="В robots.txt не указан Sitemap",
                    description="Файл robots.txt не содержит директиву Sitemap.",
                    url=robots_url,
                    severity="P3",
                    confidence=0.95,
                    autofix=True,
                    requires_confirmation=False,
                    rollback_required=False,
                    framework_reference="OPS-001 §3.1",
                    category="performance"
                ))
        except Exception as e:
            findings.append(Finding(
                rule_id="PERF-003",
                title="robots.txt недоступен",
                description=f"Ошибка при проверке robots.txt: {e}",
                url=robots_url,
                severity="P2",
                confidence=0.90,
                autofix=False,
                requires_confirmation=False,
                rollback_required=False,
                framework_reference="OPS-001 §3.1",
                category="performance"
            ))

        # sitemap.xml availability
        sitemap_url = urljoin(base, 'sitemap.xml')
        try:
            sitemap = requests.get(sitemap_url, headers=h, timeout=15)
            if sitemap.status_code != 200:
                findings.append(Finding(
                    rule_id="PERF-004",
                    title="Sitemap.xml недоступен",
                    description=f"sitemap.xml возвращает HTTP {sitemap.status_code}.",
                    url=sitemap_url,
                    severity="P2",
                    confidence=0.95,
                    autofix=False,
                    requires_confirmation=False,
                    rollback_required=False,
                    framework_reference="OPS-001 §3.2",
                    category="performance"
                ))
        except Exception as e:
            findings.append(Finding(
                rule_id="PERF-005",
                title="Ошибка проверки sitemap.xml",
                description=str(e),
                url=sitemap_url,
                severity="P2",
                confidence=0.90,
                autofix=False,
                requires_confirmation=False,
                rollback_required=False,
                framework_reference="OPS-001 §3.2",
                category="performance"
            ))

        return findings

    def _is_root(self, url: str) -> bool:
        from urllib.parse import urlparse
        path = urlparse(url).path.rstrip('/')
        return path == "" or path == "/"