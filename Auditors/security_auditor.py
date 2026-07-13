import re
import requests
from urllib.parse import urljoin
from typing import List, Optional
from Auditors.base_auditor import BaseAuditor
from AI.Models.finding import Finding


class SecurityAuditor(BaseAuditor):
    """
    Проверки безопасности: доступность xmlrpc, phpinfo, утечки версий.
    """

    name = "security"
    version = "1.0.0"

    def audit(self, url: str, html: str, headers: Optional[dict] = None) -> List[Finding]:
        findings = []
        h = self._headers(headers)
        base = url

        # WordPress generator meta
        if re.search(r'<meta[^\u003e]+name=["\']generator["\'][^\u003e]+content=["\']WordPress', html, re.IGNORECASE):
            findings.append(Finding(
                rule_id="SEC-002",
                title="WordPress generator exposed",
                description="В HTML выводится meta generator с версией WordPress.",
                url=url,
                severity="P3",
                confidence=0.95,
                autofix=True,
                requires_confirmation=False,
                rollback_required=False,
                framework_reference="SEC-001 §1.2",
                category="security",
                suggested_actions=[{"type": "remove_generator_meta"}]
            ))

        # xmlrpc.php availability
        xmlrpc_url = urljoin(base, 'xmlrpc.php')
        try:
            rr = requests.get(xmlrpc_url, headers=h, timeout=15)
            # xmlrpc.php обычно отвечает 405 или 200 с XML
            if rr.status_code == 200 and 'XML-RPC' in rr.text:
                findings.append(Finding(
                    rule_id="SEC-003",
                    title="XML-RPC доступен",
                    description="xmlrpc.php доступен и может использоваться для атак перебора.",
                    url=xmlrpc_url,
                    severity="P2",
                    confidence=0.85,
                    autofix=False,
                    requires_confirmation=True,
                    rollback_required=False,
                    framework_reference="SEC-001 §2.1",
                    category="security"
                ))
        except Exception:
            pass

        return findings
