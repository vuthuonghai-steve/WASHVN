---
skill_name: "test-skill-one"
owasp_coverage:
  - "A01:2021-Broken Access Control"
  - "A02:2021-Cryptographic Failures"
vulnerabilities:
  - id: "SEC-01"
    severity: "low"
    category: "Information Disclosure"
    description: "Verbose error messages in log."
    file: "core.py"
    line: 55
    remediation: "Disable tracebacks in production."
secret_scan:
  enabled: true
  findings_count: 0
overall_verdict: "SAFE"
---
# Security Review
This is the markdown body.
