---
name: lecture-creator
description: Guides the creation, customization, compilation, and git tracking of Beamer LaTeX presentations and lecture folders for Training Camp Argentina.
---

# Lecture Creator Skill — Training Camp Argentina

Use this skill when a user wants to initialize, modify, compile, or manage a lecture folder or LaTeX Beamer presentation in this repository.

---

## 1. Folder Initialization & Naming

When creating a new lecture, always copy the `00 - template` directory to a new folder named according to the following convention:

```
DayX-[Avanzado|Inicial]-Tema
```

Where:
* **X** is the day number (1 to 8).
* **Avanzado** or **Inicial** specifies the student level.
* **Tema** is the topic name (PascalCase, or alphanumeric hyphenated).

*Example:* `Day3-Inicial-PrefixSums` or `Day4-Avanzado-SegmentTree`.

---

## 2. Template Customization & Content Rules

Modify the following LaTeX command blocks in the new `main.tex` to configure the metadata of the class:

| Field | LaTeX Command | Example |
|---|---|---|
| Class Title | `\title{...}` | `\title{Estructuras de Datos}` |
| Student Level | `\subtitle{...}` | `\subtitle{Inicial}` |
| Author Name | `\author[Short]{Full Name}` | `\author[M. Ramos]{Matías Ramos}` |
| Institute | `\institute[]{...}` | `\institute[]{Universidad Tecnológica Nacional – FRSF}` |
| Event & Year | `\date[TC YYYY]{Training Camp YYYY}` | `\date[TC 2026]{Training Camp 2026}` |

> [!WARNING]
> Do **not** modify the ColorUNLP color theme (`#8c0011`) or the sponsor frames (`Gracias Sponsors!`) unless explicitly instructed by the repository admin.

### Pedagogical Content Rules (Especially for "Inicial" Level)
* **Code Examples:** Always try to include concrete, fully functional C++ implementation examples (using standard `block` and `verbatim` environments) to demonstrate how algorithms are coded in practice.
* **Proposed Exercises:** Always provide a final slide containing a list of 6 to 8 proposed practice problems (mainly from the CSES Problem Set) so that students can practice the concepts right after class.

---

## 3. Assets & Image Rules

* **SVG limitations:** `pdflatex` cannot compile SVGs directly. Always convert SVGs to vector PDFs or PNGs before compiling:
  ```bash
  inkscape input.svg --export-filename=output.pdf
  ```
* **Lecture Graphics:** Put all lecture-specific images inside a local `fotos/` subfolder inside the lecture directory. Reference them relative to the `main.tex` (e.g., `\includegraphics{fotos/my-image.png}`).
* **Sponsors / Logos:** Logos shared across lectures should reside in the global `/logos` folder in the root and be referenced through `\graphicspath{{../logos/}}` in the template preamble.

---

## 4. Compilation Rules

Beamer requires **two compiler passes** to resolve the slide count correctly. Always compile twice:

```bash
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

### Clean Auxiliary Files Post-Compilation
To keep the git history clean, always delete auxiliary files immediately after compiling:

```bash
rm -f main.aux main.log main.nav main.out main.toc main.vrb \
       main.snm main.fls main.fdb_latexmk main.synctex.gz
```

---

## 5. Git Tracking Rules

* **Commit auxiliary files:** Never commit auxiliary build files.
* **PDF Preview:** The compiled `main.pdf` of the template and the lecture folders are intentionally tracked on GitHub to serve as a preview. Ensure that `.gitignore` permits this via the `!**/main.pdf` rule.

---

## 6. Git Contribution Flow & PRs

If the contributor does not have write access to the upstream repository:
1. **Fork & Clone:** The agent/contributor must fork the repository and clone their fork locally.
2. **Branching:** Work must be done in a descriptive branch on the fork (e.g., `feature/dayX-lecture`).
3. **Commit & Push:** Commit changes (including the new lecture directory, `main.tex`, local `fotos/` folder, and the compiled `main.pdf`) and push them to the fork.
4. **Pull Request:** Open a Pull Request from their fork branch to the upstream `main` branch.
5. **Admin Bypass:** Only repository admins (like `matramos`) are allowed to bypass branch protection rules and push changes directly to `main`.
