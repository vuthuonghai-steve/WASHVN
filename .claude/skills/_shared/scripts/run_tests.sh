#!/bin/bash
set -e

REPO_ROOT=$(pwd)
VALIDATOR="python3 $REPO_ROOT/skills/ver-3/_shared/validators/schema_validator.py"
FIXTURES_DIR="$REPO_ROOT/skills/ver-3/_shared/fixtures"

echo "=== Running Schema Validation Tests ==="

# List of schemas and their corresponding fixtures
declare -a schemas=(
  "exploration_report:exploration_valid.md:exploration_broken_scs.md"
  "test_criteria:criteria_valid.md:criteria_broken_count.md"
  "design_doc:design_valid.md:design_broken_must_not.md"
  "quality_matrix:quality_matrix_valid.yaml:quality_matrix_broken_verdict.yaml"
  "todo_plan:todo_valid.md:todo_broken_priority.md"
  "build_log:build_log_valid.md:build_log_broken_status.md"
  "review_report:review_report_valid.md:review_report_broken_verdict.md"
  "audit_metrics:audit_metrics_valid.yaml:audit_metrics_broken_type.yaml"
  "verification_result:verification_valid.md:verification_broken_status.md"
  "security_review:security_review_valid.md:security_review_broken_verdict.md"
  "elicitation_report:elicitation_valid.md:elicitation_broken_thought.md"
  "analysis_report:analysis_valid.md:analysis_broken_metrics.md"
  "synthesis_report:synthesis_valid.md:synthesis_broken_congruence.md"
  "domain_handbook:domain_handbook_valid.md:domain_handbook_broken_glossary.md"
)

failed=0

for item in "${schemas[@]}"; do
  IFS=':' read -r artifact valid_file broken_file <<< "$item"
  
  echo -n "Testing $artifact (valid) ... "
  if $VALIDATOR --artifact "$artifact" --path "$FIXTURES_DIR/$valid_file" > /dev/null 2>&1; then
    echo "PASS"
  else
    echo "FAIL (Expected PASS)"
    failed=$((failed + 1))
  fi

  echo -n "Testing $artifact (broken) ... "
  if ! $VALIDATOR --artifact "$artifact" --path "$FIXTURES_DIR/$broken_file" > /dev/null 2>&1; then
    echo "PASS"
  else
    echo "FAIL (Expected FAIL)"
    failed=$((failed + 1))
  fi
done

echo "Registry cross-check..."
if $VALIDATOR --skills-registry > /dev/null 2>&1; then
  echo "Registry: PASS"
else
  echo "Registry: FAIL"
  failed=$((failed + 1))
fi

if [ $failed -eq 0 ]; then
  echo "All tests passed successfully!"
  exit 0
else
  echo "$failed tests failed."
  exit 1
fi
