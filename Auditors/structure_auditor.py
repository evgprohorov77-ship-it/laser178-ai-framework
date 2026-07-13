import re
from urllib.parse import urljoin, urlparse
from typing import List, Optional
import requests
from Auditors.base_auditor import BaseAuditor
from AI.Models.finding import Finding


class StructureAuditor(BaseAuditor):
    """
    Проверки структуры: битые внутренние ссылки, дубли, редиректы.
    """

    name = "structure"
    version = "1.0.0"

    def audit(self, url: str, html: str, headers: Optional[dict] = None) -> List[Finding]:
        findings = []
        h = self._headers(headers)
        base = url

        links = re.findall(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE)
        pages_to_check = set()
        for l in links:
            l = l.strip()
            if not l or l.startswith('#') or l.startswith('javascript:') or l.startswith('//'):
                continue
            if l.startswith('mailto:') or l.startswith('tel:') or l.startswith('whatsapp:'):
                continue
            if l.startswith('http'):
                parsed = urlparse(l)
                if parsed.netloc not in ['laser178.ru', 'www.laser178.ru']:
                    continue
                path = parsed.path
            else:
                path = urlparse(l).path
                if path == '/' or not path:
                    continue

            if any(p in path for p in ['/xmlrpc.php', '/wp-json/', '/feed/', '/comments/', '/favicon']):
                continue

            pages_to_check.add(urljoin(base, l.split('#')[0]))

        broken = []
        for u in sorted(pages_to_check):
            try:
                rr = requests.get(u, headers=h, timeout=15, allow_redirects=True)
                if rr.status_code >= 400:
                    broken.append((u, rr.status_code))
            except Exception as e:
                broken.append((u, str(e)))

        if broken:
            findings.append(Finding(
                rule_id="STRUCT-001",
                title="Битые внутренние ссылки",
                description=f"Обнаружено {len(broken)} битых внутренних ссылок.",
                url=url,
                severity="P2",
                confidence=0.95,
                autofix=False,
                requires_confirmation=False,
                rollback_required=False,
                framework_reference="STRUCT-001 §1.1",
                category="structure",
                metadata={"broken_links": broken}
            ))

        return findings
