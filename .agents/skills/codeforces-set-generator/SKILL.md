---
name: codeforces-set-generator
description: Generates two training contests (Inicial & Avanzado) with problems fetched from Codeforces API solved by a given user handle.
---

# Codeforces Set Generator Skill

Use this skill when asked to extract and select problems from the Codeforces API to build competitive programming training sets for a user.

---

## 1. Objectives & Behavior
Act as a Competitive Programming Expert Coach to automate problem selection for training camps.
- Target: 19 unique problems solved by the user (verdict "OK").
- **Contest Inicial (14 problems):** 2 exclusive very easy + 4 exclusive easy + 8 base common.
- **Contest Avanzado (13 problems):** 8 base common + 4 exclusive hard + 1 exclusive rating > 2000.

## 2. Rating Specifications
- **Muy Fáciles (Very Easy):** Rating == 800 (needs 2)
- **Fáciles (Easy):** 800 <= Rating <= 1100 (needs 4, distinct from very easy)
- **Base Común (Common):** 1200 <= Rating <= 1600 (needs 8)
- **Difíciles (Hard):** 1700 <= Rating <= 2100 (needs 4, distinct from very hard)
- **Muy Difíciles (Very Hard):** Rating > 2000 (needs 1)

## 3. Usage
The Python helper script is located at:
[generate_sets.py](file:///home/matias/tc-arg-2026/.agents/skills/codeforces-set-generator/scripts/generate_sets.py)

```bash
python3 .agents/skills/codeforces-set-generator/scripts/generate_sets.py <handle>
```
