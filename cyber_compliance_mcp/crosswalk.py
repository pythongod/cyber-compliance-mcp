from __future__ import annotations

from .errors import err, ok

CROSSWALK = {
    "access_control": {
        "nist_csf": ["PR.AA-01 Identity and access managed"],
        "iso27001": ["5.1 Information security policies"],
        "soc2": ["CC6 Logical and physical access controls"],
        "cis_v8": ["5.1 Account management"],
    },
    "logging_monitoring": {
        "nist_csf": ["DE.CM-01 Continuous monitoring enabled"],
        "iso27001": ["8.15 Logging", "8.16 Monitoring activities"],
        "soc2": ["CC7 System operations"],
        "cis_v8": ["8.2 Audit log management"],
    },
    "incident_response": {
        "nist_csf": ["RS.RP-01 Incident response plan executed"],
        "iso27001": ["5.7 Threat intelligence"],
        "soc2": ["CC7 System operations"],
        "cis_v8": ["17.1 Incident response process"],
    },
    "encryption": {
        "nist_csf": ["PR.AA-01 Identity and access managed"],
        "iso27001": ["8.15 Logging"],
        "soc2": ["CC6 Logical and physical access controls"],
        "cis_v8": ["3. Data Protection (mapped)"],
    },
    "vulnerability_management": {
        "nist_csf": ["DE.CM-01 Continuous monitoring enabled"],
        "iso27001": ["8.9 Configuration management"],
        "soc2": ["CC7 System operations"],
        "cis_v8": ["7. Vulnerability Management (mapped)"],
    },
    "change_management": {
        "nist_csf": ["GV.OV-01 Governance strategy defined"],
        "iso27001": ["8.9 Configuration management"],
        "soc2": ["CC8 Change management"],
        "cis_v8": ["4.1 Secure configuration process"],
    },
    "backup_recovery": {
        "nist_csf": ["RC.RP-01 Recovery plan validated"],
        "iso27001": ["8.16 Monitoring activities"],
        "soc2": ["A1 Additional criteria for availability"],
        "cis_v8": ["11. Data Recovery (mapped)"],
    },
}


def get_framework_crosswalk(topic: str) -> dict:
    key = str(topic or "").strip().lower().replace(" ", "_")
    if key not in CROSSWALK:
        return err("INVALID_TOPIC", f"Unsupported topic: {topic}", allowed=sorted(CROSSWALK.keys()))
    return ok({"topic": key, "mapping": CROSSWALK[key]})
