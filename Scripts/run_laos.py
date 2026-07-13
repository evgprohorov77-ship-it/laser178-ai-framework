#!/usr/bin/env python3
"""
Главный entrypoint LAOS Kernel.

Поток:
1. AuditRunner собирает Finding со всех аудиторов.
2. DecisionEngine принимает решение.
3. AuthorizationEngine проверяет, можно ли действовать.
4. DryRunEngine имитирует изменение.
5. ApprovalManager создаёт запрос владельцу, если нужно.
6. BackupEngine создаёт backup.
7. ActionEngine возвращает план (в MVP не применяет к сайту).
8. VerificationEngine проверяет результат.
9. Logger записывает всё.
10. GitHub Issue создаётся только для нерешённых проблем.
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
from AI.Authorization.authorization_engine import AuthorizationEngine
from AI.DryRun.dry_run_engine import DryRunEngine
from AI.Backup.backup_engine import BackupEngine
from AI.Approval.approval_manager import ApprovalManager


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def create_issue(finding, reason: str):
    print(f"\n[ISSUE] {finding.rule_id}: {finding.title}")
    print(f"  URL: {finding.url}")
    print(f"  Reason: {reason}")
    return None


def main():
    pages = [
        "https://laser178.ru/",
        "https://laser178.ru/services/",
        "https://laser178.ru/price/",
        "https://laser178.ru/calculator/",
        "https://laser178.ru/bortovoj-zhurnal/",
    ]

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    environment = load_json(os.path.join(root, "Environment", "current.json"))
    env_config = load_json(os.path.join(root, "Environment", f"{environment['active_environment']}.json"))
    capabilities = {}
    for cap_file in os.listdir(os.path.join(root, "Capabilities")):
        if cap_file.endswith(".json") and cap_file != "README.md":
            cap = load_json(os.path.join(root, "Capabilities", cap_file))
            capabilities[cap["capability"]] = cap

    approvals = ApprovalManager()

    runner = AuditRunner()
    decision_engine = DecisionEngine(framework_registry=load_json(os.path.join(root, "Registry", "rules.json")))
    risk_engine = RiskEngine()
    action_engine = ActionEngine()
    verification_engine = VerificationEngine()
    logger = Logger()
    authorization_engine = AuthorizationEngine(env_config, capabilities)
    dry_run_engine = DryRunEngine()
    backup_engine = BackupEngine()

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
        "not_authorized": 0,
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
                dry_run = dry_run_engine.run(finding)
                logger.log_event("dry_run", {"finding_id": finding.rule_id, "dry_run": dry_run})
                context = {"dry_run_uuid": dry_run["dry_run_uuid"]}

                authz = authorization_engine.authorize(finding, decision, context)
                logger.log_event("authorization", {"finding_id": finding.rule_id, "result": authz})

                if not authz["allowed"]:
                    print(f"    🚫 not authorized: {authz['reason']}")
                    stats["not_authorized"] += 1
                    if "approval" in authz["reason"].lower() or "P0" in finding.severity or "P1" in finding.severity:
                        req = approvals.create(finding, decision, dry_run)
                        print(f"    ❓ approval request: {req.uuid}")
                        stats["owner_prompts"] += 1
                    continue

                backup = backup_engine.backup(finding.url, target_type="content")
                backup_verified = backup_engine.verify(backup["backup_uuid"])
                if backup_verified["status"] != "success":
                    print(f"    🚫 backup failed: {backup_verified['reason']}")
                    create_issue(finding, backup_verified["reason"])
                    stats["issues"] += 1
                    continue
                context["backup_uuid"] = backup["backup_uuid"]

                action_result = action_engine.execute(finding, decision)
                logger.log_action(finding.rule_id, action_result)

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

    # Print waiting approvals
    waiting = approvals.list_waiting()
    if waiting:
        print("\n=== Waiting Approvals ===")
        for req in waiting:
            print(f"  {req.uuid}: {req.title} ({req.target_url})")

    # Summary
    print("\n=== LAOS Kernel Run Summary ===")
    print(f"Pages audited: {stats['audited']}")
    print(f"Findings: {stats['findings']}")
    print(f"Autofix planned: {stats['autofix']}")
    print(f"Verified: {stats['verified']}")
    print(f"Failed verification: {stats['failed']}")
    print(f"Not authorized: {stats['not_authorized']}")
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
            "session_id": logger.session_id,
            "environment": env_config["name"],
        }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
