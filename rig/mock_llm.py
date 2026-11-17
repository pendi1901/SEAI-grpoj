#!/usr/bin/env python3
"""
mock_llm.py: a stand-in for the LLM, for testing the runner offline.

Reads a prompt on stdin, prints a reply holding one fenced Python file.
It writes less code when the prompt says to reuse, so the runner's line
counts have something to measure. Special asks trigger failure cases:
an ask containing CRASH yields a program that exits 1; NOCODE yields a
reply with no code block.
"""
import re, sys

prompt = sys.stdin.read()
step = int(re.search(r"step(\d+)\.py", prompt)[1])
csvs = re.findall(r"csv file (\S+) in the current", prompt)
reuse = "Reuse the earlier files" in prompt

if "NOCODE" in prompt and "--force" not in sys.argv:
  print("I could not do that.")
  sys.exit(0)

body = [f'rows = open("{csvs[0]}").read().splitlines()',
        f'print("step {step}: saw", len(rows) - 1, "rows")']
if "CRASH" in prompt:
  body.append("raise SystemExit(1)")
if step > 1 and reuse:
  body.insert(0, "import step01")
else:
  body += [f"x{i} = {i}" for i in range(8)]       # eight lines of "glue"
print("Here is the file.\n\n```python\n# generated\n" + "\n".join(body)
      + "\n```\n")
