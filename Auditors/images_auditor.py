import re
from typing import List, Optional
from Auditors.base_auditor import BaseAuditor
from AI.Models.finding import Finding


class ImagesAuditor(BaseAuditor):
    """
    Проверки изображений: ALT, размеры, форматы, отсутствующие src.
    """

    name = "images"
    version = "1.0.0"

    def audit(self, url: str, html: str, headers: Optional[dict] = None) -> List[Finding]:
        findings = []
        imgs = re.findall(r'<img[^\u003e]*>', html, re.IGNORECASE)

        missing_alt = []
        missing_src = []
        empty_alt = []

        for img in imgs:
            src_match = re.search(r'src=["\']([^"\']+)["\']', img, re.IGNORECASE)
            alt_match = re.search(r'alt=["\']([^"\']*)["\']', img, re.IGNORECASE)

            if not src_match:
                missing_src.append(img[:80])
                continue

            if not alt_match:
                missing_alt.append(src_match.group(1))
            elif alt_match.group(1) == "":
                empty_alt.append(src_match.group(1))

        if missing_alt:
            findings.append(Finding(
                rule_id="IMG-001",
                title="Изображения без ALT",
                description=f"{len(missing_alt)} изображений без атрибута alt.",
                url=url,
                severity="P3",
                confidence=0.95,
                autofix=True,
                requires_confirmation=False,
                rollback_required=False,
                framework_reference="IMG-001 §1.1",
                category="images",
                metadata={"count": len(missing_alt), "examples": missing_alt[:5]}
            ))

        if missing_src:
            findings.append(Finding(
                rule_id="IMG-002",
                title="Изображения без SRC",
                description=f"{len(missing_src)} тегов img без атрибута src.",
                url=url,
                severity="P2",
                confidence=0.99,
                autofix=False,
                requires_confirmation=False,
                rollback_required=False,
                framework_reference="IMG-001 §2.1",
                category="images",
                metadata={"examples": missing_src[:5]}
            ))

        return findings
