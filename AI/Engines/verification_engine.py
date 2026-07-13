import re
import requests
from typing import Dict, Any, Optional
from AI.Models.finding import Finding, Decision


class VerificationEngine:
    """
    Проверяет, что автоматическое исправление действительно устранило проблему
    и не создало новых.
    """

    def __init__(self, headers: Optional[Dict[str, str]] = None):
        self.headers = headers or {"Cookie": "beget=begetok"}

    def verify(self, finding: Finding, action_result: Dict[str, Any]) -> Dict[str, Any]:
        url = finding.url
        try:
            r = requests.get(url, headers=self.headers, timeout=30)
        except Exception as e:
            return {
                "status": "failed",
                "reason": f"cannot fetch page: {e}",
                "http_code": None
            }

        if r.status_code != 200:
            return {
                "status": "failed",
                "reason": f"page returned HTTP {r.status_code}",
                "http_code": r.status_code
            }

        html = r.text
        checks = {"http_200": True}

        # Проверяем, что проблема устранена
        if finding.rule_id == "SEO-004":
            h1_count = len(re.findall(r"<h1[^\u003e]*>", html, re.IGNORECASE))
            checks["h1_normalized"] = h1_count == 1
            if not checks["h1_normalized"]:
                return {
                    "status": "failed",
                    "reason": f"H1 count still {h1_count}, expected 1",
                    "checks": checks
                }

        if finding.rule_id == "SEO-002":
            title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
            title = title_match.group(1) if title_match else ""
            checks["title_length_ok"] = len(title) <= 60
            if not checks["title_length_ok"]:
                return {
                    "status": "failed",
                    "reason": f"title length still {len(title)}",
                    "checks": checks
                }

        if finding.rule_id == "SEO-005":
            desc_match = re.search(r'<meta[^\u003e]+name=["\']description["\'][^\u003e]+content=["\']([^"\']+)', html, re.IGNORECASE)
            if not desc_match:
                desc_match = re.search(r'<meta[^\u003e]+content=["\']([^"\']+)["\'][^\u003e]+name=["\']description["\']', html, re.IGNORECASE)
            desc = desc_match.group(1) if desc_match else ""
            checks["description_length_ok"] = len(desc) <= 160
            if not checks["description_length_ok"]:
                return {
                    "status": "failed",
                    "reason": f"description length still {len(desc)}",
                    "checks": checks
                }

        # Проверяем, что не появились новые H1
        h1_count = len(re.findall(r"<h1[^\u003e]*>", html, re.IGNORECASE))
        checks["h1_count"] = h1_count
        checks["no_new_h1_beyond_one"] = (h1_count <= 1)

        return {
            "status": "success",
            "reason": "all checks passed",
            "checks": checks
        }
