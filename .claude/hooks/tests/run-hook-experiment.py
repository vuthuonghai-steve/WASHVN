#!/usr/bin/env python3
import os
import sys
import time
import json
import csv
import concurrent.futures
from anthropic import Anthropic

# Ensure API configuration
API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN")
BASE_URL = os.environ.get("ANTHROPIC_BASE_URL")

if not API_KEY:
    print("ERROR: ANTHROPIC_AUTH_TOKEN environment variable not set.")
    sys.exit(1)

client = Anthropic(api_key=API_KEY, base_url=BASE_URL)

# Fixture paths
FIXTURES_DIR = ".claude/hooks/tests/fixtures"
FIXTURES = {
    "valid": {
        "file": f"{FIXTURES_DIR}/test-SKILL-valid.md",
        "expected_ok": True
    },
    "corrupt": {
        "file": f"{FIXTURES_DIR}/test-SKILL-corrupt.md",
        "expected_ok": False
    },
    "nofrontmatter": {
        "file": f"{FIXTURES_DIR}/test-SKILL-nofrontmatter.md",
        "expected_ok": False
    }
}

# Prompt template
PROMPT_TEMPLATE = (
    "Evaluate the structural completeness of workspace documentation before session closure. "
    "Event context: $ARGUMENTS. Check for: (1) valid YAML frontmatter with all required fields "
    "(name, version, suite, tags), (2) well-formed Markdown structure (no broken tables, no unterminated "
    "code fences), (3) no dangling TODO or placeholder patterns in documentation files. "
    "Return JSON matching this schema: {\"ok\": boolean, \"reason\": string}. "
    "IMPORTANT: Return ONLY the JSON object, do not include any markdown formatting wrappers (like ```json) or explanation."
)

MODELS = {
    "haiku": "claude-3-5-haiku-20241022",
    "sonnet": "claude-3-5-sonnet-20241022"
}

def evaluate_single(model_name, model_id, fixture_name, fixture_content, expected_ok, cycle):
    # Prepare arguments JSON to replace $ARGUMENTS
    arguments_json = json.dumps({
        "files_changed": [
            {"path": f"test-SKILL-{fixture_name}.md", "content": fixture_content}
        ]
    })
    
    prompt = PROMPT_TEMPLATE.replace("$ARGUMENTS", arguments_json)
    
    start_time = time.time()
    try:
        message = client.messages.create(
            model=model_id,
            max_tokens=1000,
            temperature=0.0,
            system="You are a strict workspace documentation validator. You must output valid JSON matching the requested schema and nothing else.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        latency = (time.time() - start_time) * 1000  # in ms
        response_text = message.content[0].text.strip()
        
        # Clean up possible markdown fences
        if response_text.startswith("```"):
            lines = response_text.splitlines()
            if lines[0].startswith("```json") or lines[0].startswith("```"):
                response_text = "\n".join(lines[1:-1]).strip()
                
        res = json.loads(response_text)
        ok = bool(res.get("ok"))
        reason = res.get("reason", "")
        match = (ok == expected_ok)
        
        return {
            "model": model_name,
            "fixture": fixture_name,
            "cycle": cycle,
            "latency_ms": latency,
            "ok": ok,
            "expected_ok": expected_ok,
            "match": match,
            "reason": reason,
            "error": ""
        }
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        return {
            "model": model_name,
            "fixture": fixture_name,
            "cycle": cycle,
            "latency_ms": latency,
            "ok": False,
            "expected_ok": expected_ok,
            "match": False,
            "reason": "",
            "error": str(e)
        }

def main():
    print("=== Starting 60-Cycle Hook Experiment ===")
    
    # Read fixtures
    fixture_contents = {}
    for name, info in FIXTURES.items():
        try:
            with open(info["file"], "r") as f:
                fixture_contents[name] = f.read()
        except Exception as e:
            print(f"ERROR: Cannot read fixture {info['file']}: {e}")
            sys.exit(1)
            
    tasks = []
    # 2 models * 3 fixtures * 10 cycles = 60 tasks
    for model_name, model_id in MODELS.items():
        for fixture_name, content in fixture_contents.items():
            expected_ok = FIXTURES[fixture_name]["expected_ok"]
            for cycle in range(1, 11):
                tasks.append((model_name, model_id, fixture_name, content, expected_ok, cycle))
                
    results = []
    print(f"Queueing {len(tasks)} evaluations using thread pool...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(evaluate_single, *task): task for task in tasks
        }
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            res = future.result()
            results.append(res)
            print(f"[{i}/{len(tasks)}] Model: {res['model']}, Fixture: {res['fixture']}, Latency: {res['latency_ms']:.0f}ms, Ok: {res['ok']}, Match: {res['match']}")
            
    # Save CSV
    csv_file = ".claude/hooks/tests/experiment-results.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["model", "fixture", "cycle", "latency_ms", "ok", "expected_ok", "match", "reason", "error"])
        writer.writeheader()
        for r in results:
            writer.writerow(r)
            
    print(f"\nExperiment complete. Results saved to {csv_file}")
    
    # Calculate statistics
    stats = {}
    for m in MODELS:
        stats[m] = {}
        for f in FIXTURES:
            stats[m][f] = {
                "latencies": [],
                "matches": 0,
                "ok_count": 0,
                "total": 0
            }
            
    for r in results:
        m = r["model"]
        f = r["fixture"]
        stats[m][f]["latencies"].append(r["latency_ms"])
        if r["match"]:
            stats[m][f]["matches"] += 1
        if r["ok"]:
            stats[m][f]["ok_count"] += 1
        stats[m][f]["total"] += 1
        
    # Print summary table
    print("\n=== Experiment Summary ===")
    for m in MODELS:
        print(f"\nModel: {m}")
        for f in FIXTURES:
            lats = sorted(stats[m][f]["latencies"])
            p50 = lats[len(lats)//2]
            p95 = lats[int(len(lats)*0.95)]
            p99 = lats[int(len(lats)*0.99)]
            acc = (stats[m][f]["matches"] / stats[m][f]["total"]) * 100
            print(f"  Fixture '{f}': Accuracy: {acc:.0f}%, P50 Latency: {p50:.0f}ms, P95: {p95:.0f}ms, P99: {p99:.0f}ms")

if __name__ == "__main__":
    main()
