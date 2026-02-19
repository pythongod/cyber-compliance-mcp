from __future__ import annotations

from typing import Dict

CONTROL_METADATA: Dict[str, Dict[str, Dict[str, str]]] = {
    "nist_csf": {
        "GV.OV-01 Governance strategy defined": {
            "owner": "security-lead",
            "priority": "high",
            "evidence_example": "Approved security governance charter",
        },
        "ID.AM-01 Asset inventory maintained": {
            "owner": "it-ops",
            "priority": "high",
            "evidence_example": "CMDB export with asset owners",
        },
        "PR.AA-01 Identity and access managed": {
            "owner": "iam",
            "priority": "critical",
            "evidence_example": "MFA policy and IdP configuration screenshots",
        },
        "DE.CM-01 Continuous monitoring enabled": {
            "owner": "secops",
            "priority": "high",
            "evidence_example": "SIEM dashboards + alert routing evidence",
        },
        "RS.RP-01 Incident response plan executed": {
            "owner": "security",
            "priority": "high",
            "evidence_example": "IR runbook and tabletop exercise record",
        },
        "RC.RP-01 Recovery plan validated": {
            "owner": "it-ops",
            "priority": "medium",
            "evidence_example": "Backup restore test results",
        },
    },
    "iso27001": {
        "5.1 Information security policies": {
            "owner": "security-governance",
            "priority": "high",
            "evidence_example": "Signed information security policy",
        },
        "5.7 Threat intelligence": {
            "owner": "secops",
            "priority": "medium",
            "evidence_example": "Threat feed subscriptions and review logs",
        },
        "8.9 Configuration management": {
            "owner": "platform-engineering",
            "priority": "high",
            "evidence_example": "Baseline config standards and drift reports",
        },
        "8.15 Logging": {
            "owner": "secops",
            "priority": "high",
            "evidence_example": "Centralized logging retention policy",
        },
        "8.16 Monitoring activities": {
            "owner": "secops",
            "priority": "high",
            "evidence_example": "Monitoring coverage matrix",
        },
        "8.23 Web filtering": {
            "owner": "network-security",
            "priority": "medium",
            "evidence_example": "Web proxy policy and blocked domain reports",
        },
    },
    "soc2": {
        "CC1 Control environment": {
            "owner": "leadership",
            "priority": "high",
            "evidence_example": "Code of conduct and governance reviews",
        },
        "CC2 Communication and information": {
            "owner": "security",
            "priority": "medium",
            "evidence_example": "Security awareness and policy communication logs",
        },
        "CC6 Logical and physical access controls": {
            "owner": "iam",
            "priority": "critical",
            "evidence_example": "Access review reports + MFA enforcement",
        },
        "CC7 System operations": {
            "owner": "secops",
            "priority": "high",
            "evidence_example": "Ops monitoring and incident tickets",
        },
        "CC8 Change management": {
            "owner": "engineering",
            "priority": "high",
            "evidence_example": "PR approvals and deployment change records",
        },
        "A1 Additional criteria for availability": {
            "owner": "sre",
            "priority": "medium",
            "evidence_example": "SLA/SLO reports and outage postmortems",
        },
    },
    "cis_v8": {
        "1.1 Inventory and control of enterprise assets": {
            "owner": "it-ops",
            "priority": "high",
            "evidence_example": "Asset inventory snapshots",
        },
        "4.1 Secure configuration process": {
            "owner": "platform-engineering",
            "priority": "high",
            "evidence_example": "Configuration hardening standards",
        },
        "5.1 Account management": {
            "owner": "iam",
            "priority": "critical",
            "evidence_example": "Joiner/mover/leaver workflow evidence",
        },
        "8.2 Audit log management": {
            "owner": "secops",
            "priority": "high",
            "evidence_example": "Log retention policy + SIEM export",
        },
        "12.1 Network infrastructure management": {
            "owner": "network-engineering",
            "priority": "medium",
            "evidence_example": "Network device inventory and configs",
        },
        "17.1 Incident response process": {
            "owner": "security",
            "priority": "high",
            "evidence_example": "Incident response procedure and exercise notes",
        },
    },
}
