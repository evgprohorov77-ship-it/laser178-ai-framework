import re
from typing import List, Optional
from Auditors.base_auditor import BaseAuditor
from AI.Models.finding import Finding


class SEOAuditor(BaseAuditor):
    """
    Проверки SEO: title, description, H1, canonical, Open Graph.
    """

    name = "seo"
    version = "1.0.0"

    def audit(self, url: str, html: str, headers: Optional[dict] = None) -> List[Finding]:
        findings = []

        # Title length
        title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
        title = title_match.group(1) if title_match else ""
        if title and len(title) > 60:
            findings.append(Finding(
                rule_id="SEO-002",
                title="Title длиннее 60 символов",
                description=f"Title страницы содержит {len(title)} символов и может обрезаться в выдаче.",
                url=url,
                severity="P2",
                confidence=1.0,
                autofix=True,
                requires_confirmation=False,
                rollback_required=False,
                framework_reference="SEO-001 §2.1",
                category="seo",
                metadata={"current_title": title, "length": len(title)},
                suggested_actions=[{"type": "edit_title", "max_length": 60}]
            ))
        elif not title:
            findings.append(Finding(
                rule_id="SEO-003",
                title="Title отсутствует",
                description="На странице не заполнен тег title.",
                url=url,
                severity="P2",
                confidence=1.0,
                autofix=True,
                requires_confirmation=False,
                rollback_required=False,
                framework_reference="SEO-001 §2.1",
                category="seo",
                suggested_actions=[{"type": "edit_title"}]
            ))

        # Description length
        desc_match = re.search(r'<meta[^\u003e]+name=["\']description["\'][^\u003e]+content=["\']([^"\']+)', html, re.IGNORECASE)
        if not desc_match:
            desc_match = re.search(r'<meta[^\u003e]+content=["\']([^"\']+)["\'][^\u003e]+name=["\']description["\']', html, re.IGNORECASE)
        desc = desc_match.group(1) if desc_match else ""
        if desc and len(desc) > 160:
            findings.append(Finding(
                rule_id="SEO-005",
                title="Description длиннее 160 символов",
                description=f"Meta description содержит {len(desc)} символов.",
                url=url,
                severity="P2",
                confidence=1.0,
                autofix=True,
                requires_confirmation=False,
                rollback_required=False,
                framework_reference="SEO-001 §2.2",
                category="seo",
                metadata={"current_description": desc, "length": len(desc)},
                suggested_actions=[{"type": "edit_description", "max_length": 160}]
            ))
        elif not desc:
            findings.append(Finding(
                rule_id="SEO-006",
                title="Description отсутствует",
                description="На странице не заполнен meta description.",
                url=url,
                severity="P2",
                confidence=1.0,
                autofix=True,
                requires_confirmation=False,
                rollback_required=False,
                framework_reference="SEO-001 §2.2",
                category="seo"
            ))

        # H1 count
        h1_count = len(re.findall(r"<h1[^\u003e]*>", html, re.IGNORECASE))
        if h1_count != 1:
            findings.append(Finding(
                rule_id="SEO-004",
                title="Дублирующийся или отсутствующий H1",
                description=f"На странице обнаружено {h1_count} тегов H1. Должен быть ровно один.",
                url=url,
                severity="P2",
                confidence=0.98,
                autofix=True,
                requires_confirmation=False,
                rollback_required=False,
                framework_reference="SEO-001 §4.3",
                category="seo",
                metadata={"h1_count": h1_count},
                suggested_actions=[{"type": "normalize_h1"}]
            ))

        # Missing canonical
        if not re.search(r'<link[^\u003e]+rel=["\']canonical["\']', html, re.IGNORECASE):
            findings.append(Finding(
                rule_id="SEO-007",
                title="Отсутствует canonical URL",
                description="На странице не указан canonical link.",
                url=url,
                severity="P3",
                confidence=0.95,
                autofix=True,
                requires_confirmation=False,
                rollback_required=False,
                framework_reference="SEO-001 §5.1",
                category="seo",
                suggested_actions=[{"type": "add_canonical"}]
            ))

        return findings
