#!/usr/bin/env bash
# Integration test to verify prompt-based Stop hook self-healing using real Claude CLI
set -e

echo "=== Running Claude CLI Hook Integration Tests ==="

# Clean up any existing test files
rm -f test_doc.md

# 1. Test case: Valid document (should pass validation immediately, exit normally)
echo "--- Testing Valid Fixture ---"
cp .claude/hooks/tests/fixtures/test-SKILL-valid.md test_doc.md
# Run Claude Code to read the file. Since it is valid, it should not trigger any block.
rtk proxy claude --permission-mode bypassPermissions -p "Read test_doc.md, verify it is completely valid, and exit."
echo "Valid fixture test: PASS"

# 2. Test case: Corrupt document (should trigger Stop hook block and self-heal)
echo "--- Testing Corrupt Fixture (Self-Healing) ---"
cp .claude/hooks/tests/fixtures/test-SKILL-corrupt.md test_doc.md

# Run Claude Code. Tell it to read the file and let it handle the Stop hook block.
# Since continueOnBlock: true is set, when the agent tries to exit, it will receive the hook feedback,
# then it must use its tools to edit and fix the file before it can exit successfully.
rtk proxy claude --permission-mode bypassPermissions -p "Read test_doc.md. If you receive any Stop hook feedback about document corruption, immediately use the Edit/Write tool to fix the YAML frontmatter and remove the TODO placeholder in test_doc.md, then exit."

# Verify that test_doc.md has been corrected on disk
if grep -q "TODO" test_doc.md; then
  echo "FAIL: test_doc.md still contains TODO placeholder"
  exit 1
fi
if grep -q 'description: "Corrupt test file with multiple issues$' test_doc.md; then
  echo "FAIL: test_doc.md frontmatter description is still unclosed"
  exit 1
fi

echo "Corrupt fixture self-healing test: PASS"

# Clean up
rm -f test_doc.md
echo "=== All integration tests PASSED successfully ==="
