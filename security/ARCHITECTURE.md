security/
│
├── README.md
├── ARCHITECTURE.md
├── DESIGN.md
├── manifest.yaml
├── __init__.py
│
├── core/
│   ├── security_manager.py
│   ├── security_registry.py
│   ├── security_resolver.py
│   ├── security_builder.py
│   ├── security_validator.py
│   ├── security_policy.py
│   └── exceptions.py
│
├── identity/
│   ├── identity.py
│   ├── principal.py
│   ├── authentication.py
│   ├── authorization.py
│   ├── roles.py
│   ├── permissions.py
│   └── sessions.py
│
├── governance/
│   ├── governance_policy.py
│   ├── trust_policy.py
│   ├── ethics_policy.py
│   ├── compliance_policy.py
│   ├── ai_policy.py
│   └── data_policy.py
│
├── access/
│   ├── access_controller.py
│   ├── access_rules.py
│   ├── resource_guard.py
│   └── repository_guard.py
│
├── privacy/
│   ├── pii_detector.py
│   ├── anonymizer.py
│   ├── pseudonymizer.py
│   ├── consent_manager.py
│   └── retention_policy.py
│
├── integrity/
│   ├── checksum.py
│   ├── signatures.py
│   ├── verification.py
│   ├── tamper_detection.py
│   └── provenance_verifier.py
│
├── cryptography/
│   ├── encryption.py
│   ├── decryption.py
│   ├── key_manager.py
│   ├── certificate_manager.py
│   └── vault.py
│
├── audit/
│   ├── audit_logger.py
│   ├── audit_repository.py
│   ├── audit_report.py
│   ├── immutable_log.py
│   └── evidence_chain.py
│
├── monitoring/
│   ├── threat_detector.py
│   ├── anomaly_detector.py
│   ├── intrusion_detector.py
│   ├── security_monitor.py
│   └── alert_manager.py
│
├── ai/
│   ├── prompt_guard.py
│   ├── jailbreak_detector.py
│   ├── hallucination_guard.py
│   ├── model_guard.py
│   ├── output_filter.py
│   └── risk_assessor.py
│
├── contracts/
│   ├── security_result.py
│   ├── authorization_result.py
│   ├── authentication_result.py
│   ├── audit_result.py
│   └── risk_result.py
│
└── tests/
