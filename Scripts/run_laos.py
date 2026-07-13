#!/usr/bin/env python3
"""
Главный entrypoint LAOS.

Поток:
1. AuditRunner собирает Finding со всех аудиторов.
2. DecisionEngine принимает решение по каждому.
3. RiskEngine оценивает риск.
4. ActionEngine выполняет одобренные autofix.
5. VerificationEngine проверяет результат.
6. Logger записывает всё.
7. GitHub Issue создаётся только для нерешённых проблем.
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Auditors.runner import AuditRunner
from AI.Decision.decision_engine import DecisionEngine
from AI.Engines.risk_engine import RiskEngine
from AI.Engines.action_engine import ActionEngine
from AI.Engines.verification_engine import VerificationEngine
from AI.Engines.logger import Logger


def load_rules():
    path = os.path.join(os.path.dirname(__file__), "..", "Registry", "rules.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def create_issue(finding, reason: str):
    # В MVP — печать в консоль. В продакшене — POST в GitHub API.
    print(f"\n[ISSUE] {finding.rule_id}: {finding.title}")
    print(f"  URL: {finding.url}")
    print(f"  Reason: {reason}")
    return None  # номер issue


def main():
    pages = [
        "https://laser178.ru/",
        "https://laser178.ru/services/",
        "https://laser178.ru/price/",
        "https://laser178.ru/calculator/",
        "https://laser178.ru/bortovoj-zhurnal/",
    ]

    runner = AuditRunner()
    decision_engine = DecisionEngine(framework_registry=load_rules())
    risk_engine = RiskEngine()
    action_engine = ActionEngine()
    verification_engine = VerificationEngine()
    logger = Logger()

    stats = {
        "audited": 0,
        "findings": 0,
        "autofix": 0,
        "verified": 0,
        "failed": 0,
        "issues": 0,
        "owner_prompts": 0,
        "rejected": 0,
        "framework_improvements": 0,
    }

    for url in pages:
        stats["audited"] += 1
        print(f"\n=== Auditing {url} ===")
        findings = runner.run_page(url)
        logger.log_audit(findings)
        stats["findings"] += len(findings)

        for finding in findings:
            decision = decision_engine.decide(finding)
            logger.log_decision(finding.rule_id, decision)
            risk = risk_engine.assess(finding, decision)

            print(f"  {finding.severity} {finding.rule_id}: {decision.action} (risk={risk['final_risk']}, conf={finding.confidence})")

            if decision.action == "autofix":
                action_result = action_engine.execute(finding, decision)
                logger.log_action(finding.rule_id, action_result)

                if action_result["status"] == "planned":
                    # В MVP не применяем изменения к сайту, только проверяем текущее состояние
                    verify_result = verification_engine.verify(finding, action_result)
                    logger.log_verification(finding.rule_id, verify_result)

                    if verify_result["status"] == "success":
                        stats["verified"] += 1
                        print(f"    ✅ verified: {verify_result['reason']}")
                    else:
                        stats["failed"] += 1
                        print(f"    ❌ verification failed: {verify_result['reason']}")
                        create_issue(finding, verify_result["reason"])
                        logger.log_issue(finding.rule_id, 0, verify_result["reason"])
                        stats["issues"] += 1
                else:
                    create_issue(finding, action_result["reason"])
                    logger.log_issue(finding.rule_id, 0, action_result["reason"])
                    stats["issues"] += 1

                stats["autofix"] += 1

            elif decision.action == "issue":
                create_issue(finding, decision.reason)
                logger.log_issue(finding.rule_id, 0, decision.reason)
                stats["issues"] += 1

            elif decision.action == "ask":
                print(f"    ❓ owner prompt: {decision.owner_prompt}")
                stats["owner_prompts"] += 1

            elif decision.action == "reject":
                print(f"    🚫 rejected: {decision.reason}")
                stats["rejected"] += 1

            elif decision.action == "framework_improvement":
                create_issue(finding, f"Missing framework reference: {finding.framework_reference}")
                logger.log_issue(finding.rule_id, 0, f"Missing framework reference: {finding.framework_reference}")
                stats["framework_improvements"] += 1

    # Summary
    print("\n=== LAOS Run Summary ===")
    print(f"Pages audited: {stats['audited']}")
    print(f"Findings: {stats['findings']}")
    print(f"Autofix planned: {stats['autofix']}")
    print(f"Verified: {stats['verified']}")
    print(f"Failed verification: {stats['failed']}")
    print(f"Issues created: {stats['issues']}")
    print(f"Owner prompts: {stats['owner_prompts']}")
    print(f"Rejected: {stats['rejected']}")
    print(f"Framework improvements: {stats['framework_improvements']}")
    print(f"Logs: {logger.log_dir}/{logger.session_id}")

    summary_path = os.path.join(logger.log_dir, logger.session_id, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "stats": stats,
            "session_id": logger.session_id
        }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
