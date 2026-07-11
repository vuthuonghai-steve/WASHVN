# Design Checklist (pre-deliver gate)
# [TỬ DESIGN §8 R4-R6] [TỬ TODO #T5.1]
Run against every produced hook spec BEFORE writing to settings.json.

- [ ] Event is one of 30 canonical events (canonical-events.yaml)
- [ ] If event chosen does not support matcher, matcher field omitted
- [ ] Matcher classified (exact_or | regex) via matcher_classifier.py
- [ ] Footgun warning shown if matcher contains '.' (forced regex)
- [ ] Handler type in {command, prompt, agent}
- [ ] Blocking requested ONLY on PreToolUse (else reject)
- [ ] Dual-format: Format A XOR Format B selected, NOT mixed
- [ ] continueOnBlock=true ONLY on Stop / SubagentStop (else reject)
- [ ] if-condition uses allowed operators (== != =~ in) + context vars
- [ ] Target location resolved; shadowing warning shown if higher priority collides
- [ ] No TODO / FIXME / placeholder in handler impl
- [ ] Auto-write will use backup + diff-preview + fail-closed (settings_writer.py)

# Any unchecked critical item => halt, do not write.
