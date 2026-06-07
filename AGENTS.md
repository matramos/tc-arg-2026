# AGENTS.md — AI Agent Rules for tc-arg-2026

This file defines mandatory rules for any AI agent (Claude, Gemini, Copilot, etc.)
working inside this repository.

---

## Project Context

This is a **LaTeX Beamer presentation template** repository for the
**Training Camp Argentina 2026 (TC ARG 2026)** competitive programming camp,
hosted at UNLP – Facultad de Informática.

- Main template: `00 - template/main.tex`
- Engine: `pdflatex`
- Document class: `beamer` (Madrid theme, UNLP bordeaux color `#8c0011`)

---

## Compilation Rules

### ⚠️ ALWAYS compile twice

Beamer requires two `pdflatex` passes to correctly resolve the total frame count
in the footer (`\inserttotalframenumber`). A single pass will always show `1`
as the total number of slides.

```bash
cd "00 - template"
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

### ⚠️ ALWAYS clean auxiliary files after compilation

Never commit LaTeX auxiliary files. After every compilation run:

```bash
rm -f main.aux main.log main.nav main.out main.toc main.vrb \
       main.snm main.fls main.fdb_latexmk main.synctex.gz
```

---

## File & Asset Rules

- **SVG files cannot be used directly** with `pdflatex`. Always convert SVGs to PDF
  (vector, preferred) or PNG before referencing them in `\includegraphics{}`.
  Use Inkscape for conversion:
  ```bash
  inkscape input.svg --export-filename=output.pdf
  ```
- After adding a new PDF logo asset, add an exception to `.gitignore`:
  ```
  !logos/your-logo.pdf
  ```
- The compiled `main.pdf` and `logoTC.pdf` are intentionally tracked in git as a
  preview for contributors. All other `*.pdf` files are ignored.

---

## Git & Branch Rules

- The `main` branch is **protected**. Never push directly to `main` on behalf of
  non-admin users. Changes must go through a Pull Request.
- The repository owner (`matramos`) has admin bypass and may push directly.
- Commit messages must be descriptive and in English.
- Never commit auxiliary LaTeX build files (`*.aux`, `*.log`, `*.nav`, etc.);
  they are covered by `.gitignore`.

## Folder Naming Rules

When initializing a new lecture folder by copying the `00 - template` directory, you **must** use the following naming format:
`DayX-[Avanzado|Inicial]-Tema`

Where:
* `X` is the day number (1 to 8).
* `Avanzado` or `Inicial` specifies the student level.
* `Tema` is the topic name (PascalCase, or alphanumeric hyphenated).

Example folder names:
* `Day1-Inicial-BusquedaBinaria`
* `Day2-Avanzado-SegmentTree`

---

## Template Customization Rules

When modifying `main.tex` for a new class edition, the following fields
**must** be updated:

| Field | LaTeX command |
|---|---|
| Class title | `\title{...}` |
| Subtitle | `\subtitle{...}` |
| Author | `\author[Short]{Full Name}` |
| Institute | `\institute[]{...}` |
| Event name + year | `\date[TC YYYY]{Training Camp YYYY}` |
| Section names | `\section{Real Topic Name}` |

Do **not** modify the color theme (`ColorUNLP` / `#8c0011`) or the sponsor frames
without explicit user instruction — these reflect the official identity of the event.

---

## Logos

All active logos are stored in logos/. Do not delete or rename
any of these files without updating the corresponding `\includegraphics{}` calls
in `main.tex` and recompiling to verify.

| File | Purpose |
|---|---|
| `logo_aapc.png` | AAPC organizer logo |
| `logoTC.pdf` | TC Argentina logo (vector) |
| `unlp_informatica.png` | UNLP Facultad de Informática logo |
| `unlp.png` | UNLP general logo |
| `GTSlogo.jpeg` | GTS Diamond Sponsor logo |
| `icpc.jpeg` | ICPC logo |
