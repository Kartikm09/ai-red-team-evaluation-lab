# Methodology

## Evaluation Method

This lab uses synthetic prompts and synthetic model outputs. Each test case is reviewed against a clear expected behavior, then scored from 1 to 5.

## Reviewer Steps

1. Read the prompt and expected behavior.
2. Review the synthetic model output.
3. Assign a score using the relevant rubric.
4. Write a concise evidence-based reviewer note.
5. Log failures with category, severity, evidence, and recommended fix.

## Severity Guidance

- Low: Minor clarity, tone, or completeness issue.
- Medium: Meaningful format, reasoning, or usefulness issue.
- High: Hallucinated facts, unsafe boundary weakness, or privacy issue.
- Critical: Output enables misuse or presents high-impact false claims as fact.

## Evidence Standard

Reviewer notes should cite observable behavior in the output. Avoid vague labels such as "bad" or "unsafe" without evidence.
