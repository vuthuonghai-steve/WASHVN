# OWASP Security Checklist — Full 10 Categories

> **Purpose**: Comprehensive security checklist for AI Agent skills
> **Severity Levels**: CRITICAL > HIGH > MEDIUM > LOW > INFO

---

## OWASP Top 10 (2021) — Abbreviated for AI Skills

### 1. Broken Access Control (CRITICAL)
| Check | Severity | Description |
|-------|----------|-------------|
| AC-01 | CRITICAL | Authentication required where needed |
| AC-02 | HIGH | Authorization checks on all operations |
| AC-03 | HIGH | No IDOR (Insecure Direct Object Reference) |
| AC-04 | MEDIUM | Session management secure |

### 2. Cryptographic Failures (CRITICAL)
| Check | Severity | Description |
|-------|----------|-------------|
| CF-01 | CRITICAL | No hardcoded secrets in code |
| CF-02 | CRITICAL | Environment variables for secrets |
| CF-03 | HIGH | No credentials in logs |
| CF-04 | MEDIUM | Crypto keys properly generated |

### 3. Injection (CRITICAL)
| Check | Severity | Description |
|-------|----------|-------------|
| IN-01 | CRITICAL | No string concatenation in commands |
| IN-02 | HIGH | Parameterized queries only |
| IN-03 | HIGH | Input validation on all paths |
| IN-04 | MEDIUM | Output encoding appropriate |

### 4. Insecure Design (HIGH)
| Check | Severity | Description |
|-------|----------|-------------|
| ID-01 | HIGH | No security anti-patterns created |
| ID-02 | MEDIUM | Sandbox specified for execution |
| ID-03 | MEDIUM | Rate limiting documented |

### 5. Security Misconfiguration (MEDIUM)
| Check | Severity | Description |
|-------|----------|-------------|
| SM-01 | HIGH | Docker/gVisor sandbox for scripts |
| SM-02 | MEDIUM | No default credentials |
| SM-03 | MEDIUM | Error messages sanitized |
| SM-04 | LOW | Debug mode disabled in production |

### 6. Vulnerable Components (MEDIUM)
| Check | Severity | Description |
|-------|----------|-------------|
| VC-01 | HIGH | No known vulnerable libraries |
| VC-02 | MEDIUM | Dependencies documented |

### 7. Authentication Failures (HIGH)
| Check | Severity | Description |
|-------|----------|-------------|
| AF-01 | HIGH | Password policy enforced |
| AF-02 | MEDIUM | Account lockout configured |
| AF-03 | LOW | MFA available if critical |

### 8. Software/Data Integrity (MEDIUM)
| Check | Severity | Description |
|-------|----------|-------------|
| SD-01 | HIGH | No unsigned code execution |
| SD-02 | MEDIUM | Update mechanism verified |

### 9. Logging & Monitoring (MEDIUM)
| Check | Severity | Description |
|-------|----------|-------------|
| LM-01 | MEDIUM | Security events logged |
| LM-02 | LOW | Anomaly detection present |

### 10. SSRF (Server-Side Request Forgery) (HIGH)
| Check | Severity | Description |
|-------|----------|-------------|
| SS-01 | HIGH | URL validation before fetch |
| SS-02 | MEDIUM | Allowlist for external requests |

---

## AI-Specific Security Checks

### Prompt Injection Defense
| Check | Severity | Description |
|-------|----------|-------------|
| PI-01 | CRITICAL | User input separated from system prompts |
| PI-02 | HIGH | No direct echo of untrusted input |
| PI-03 | MEDIUM | Output validation on generated code |

### Tool/Script Security
| Check | Severity | Description |
|-------|----------|-------------|
| TS-01 | CRITICAL | Scripts run in sandbox |
| TS-02 | HIGH | No rm -rf / accident prevention |
| TS-03 | MEDIUM | Resource limits set |

---

## Severity Response Time

| Severity | Response |
|----------|----------|
| CRITICAL | Fix immediately, block release |
| HIGH | Fix within 24 hours |
| MEDIUM | Fix within 1 week |
| LOW | Fix within 1 month |
| INFO | Address when convenient |

---

> **Last Updated**: 2026-06-03
