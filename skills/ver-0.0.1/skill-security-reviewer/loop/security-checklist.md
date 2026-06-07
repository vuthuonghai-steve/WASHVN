# Security Review Checklist

> **Purpose**: Interactive checklist for security review workflow

---

## Pre-Review Setup

- [ ] Identify skill type: auth | payment | upload | manual
- [ ] Read skill's design.md §8 (Risk Matrix)
- [ ] Check if skill creates executable scripts

---

## Automated Checks

### SEC-01: Broken Access Control
- [ ] AC-01: Authentication required? Yes/No/N/A
- [ ] AC-02: Authorization validated? Yes/No/N/A
- [ ] AC-03: No IDOR vulnerabilities? Yes/No/N/A

### SEC-02: Cryptographic Failures
- [ ] CF-01: No hardcoded secrets? Yes/No/N/A
- [ ] CF-02: Environment variables for secrets? Yes/No/N/A
- [ ] CF-03: No credentials in logs? Yes/No/N/A

### SEC-03: Injection
- [ ] IN-01: No string concat in commands? Yes/No/N/A
- [ ] IN-02: Parameterized queries? Yes/No/N/A
- [ ] IN-03: Input validation present? Yes/No/N/A

### SEC-04: Insecure Design
- [ ] ID-01: No security anti-patterns? Yes/No/N/A
- [ ] ID-02: Sandbox specified? Yes/No/N/A

### SEC-05: Security Misconfiguration
- [ ] SM-01: Docker sandbox for scripts? Yes/No/N/A
- [ ] SM-02: No default credentials? Yes/No/N/A
- [ ] SM-03: Error messages sanitized? Yes/No/N/A

---

## Output Generation

After completing checks, generate report:

```
=== SECURITY REVIEW REPORT ===
Skill: {name}
Timestamp: {date}
Trigger: {type}

Verdict: APPROVED | REQUEST CHANGES | REJECTED

Critical Findings: {count}
High Findings: {count}
Medium Findings: {count}
Low Findings: {count}

Action Required: {yes|no}
```

---

## Review Completion

- [ ] Report generated
- [ ] Result logged to .skill-context/{target_skill}/security-review-report.md
- [ ] If APPROVED → Continue to Gatekeeper
- [ ] If REQUEST CHANGES → Block until fixed
- [ ] If REJECTED → Rollback to Architect

---

> **Last Updated**: 2026-06-03
