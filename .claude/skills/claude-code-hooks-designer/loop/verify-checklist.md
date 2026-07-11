# Verification Checklist (REAL execution)
# [TỬ DESIGN §8 R7, HOOK-1.07] [TỬ TODO #T5.2] [TỬ HANDBOOK §7.4]
Run scripts/verify_hook.py — it spawns the real hook, not a lint.

- [ ] Hook script materialized to disk (not inline mock)
- [ ] Hook invoked with real stdin JSON (tool/params)
- [ ] Activation observed (process ran, produced output/exit)
- [ ] Block case: exit code == 2 (Format B) or exit 0 + JSON deny (Format A)
- [ ] Allow case: exit code == 0
- [ ] Verification report records: hook path, event, matcher match, decision, result
- [ ] Report printed to user with PASS/FAIL

# Any FAIL => build blocked, do not deliver.
