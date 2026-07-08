---
name: test-skill-corrupt
description: "Corrupt test file with multiple issues
version: 1.0.0   # Thiếu dấu " đóng ở description
suite: WASHVN
tags: [test, corrupt
when_to_use: "Use for testing corrupt file detection"
---

# Test Skill Corrupt

This file has multiple structural issues.

## Unclosed Code Fence

```python
def hello():
    print("hello")
`  <!-- Thiếu closing mark -->

## Broken Table

| Header 1 | Header 2 |
|----------|----------|
| Cell 1  | Cell 2
| Cell 3  | Cell 4 |  <!-- Thiếu pipe ở row 1 -->

## TODO Placeholder

TODO: implement this section
