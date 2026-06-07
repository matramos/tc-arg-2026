# Training Camp Argentina 2026 — Slide Template

Official Beamer slide template for the **Training Camp Argentina 2026** (TC ARG 2026),
hosted by the **Universidad Nacional de La Plata – Facultad de Informática**.

Organized by [AAPC](https://aapc.com.ar) · Diamond Sponsor: GTS

---

## Repository Structure

```
tc-arg-2026/
├── logos/                # Shared repository logos — ONE copy for all classes!
│   ├── logo_aapc.png         # AAPC organizer logo
│   ├── logoTC.pdf            # TC Argentina logo (vector)
│   ├── unlp_informatica.png  # UNLP Facultad de Informática logo
│   ├── unlp.png              # UNLP general logo
│   ├── GTSlogo.jpeg          # GTS Diamond Sponsor logo
│   └── icpc.jpeg             # ICPC logo
└── 00 - template/
    ├── main.tex          # Main Beamer template — copy this for each new class
    └── main.pdf          # Compiled preview of the template
```

---

## Creating a New Class

1. **Copy the template folder** and rename it using the naming convention: `DayX-[Avanzado|Inicial]-Tema`
   
   * `X` represents the day of the lecture (from 1 to 8).
   * Track is either `Avanzado` or `Inicial`.
   * Tema is the topic of the class (without spaces, using PascalCase or hyphens).

   Example folder names:
   * `Day1-Inicial-BusquedaBinaria`
   * `Day1-Avanzado-SegmentTree`

   ```bash
   cp -r "00 - template" "Day1-Inicial-BusquedaBinaria"
   ```

2. **Edit `main.tex`**:
   - Set the class title: `\title{Tu Título Aquí}`
   - Set the subtitle: `\subtitle{(Subtítulo opcional)}`
   - Set the author: `\author[Nombre Corto]{Nombre Completo}`
   - Rename sections: `\section{Nombre del Tema}` — the outline slides update automatically.
   - Replace placeholder frames with your content.

3. **Compile** (see below).

---

## Compilation — ⚠️ Two Passes Required

Beamer requires **two `pdflatex` compilations** for the footer to display the correct
total number of slides. A single run will always show `1` as the total.

```bash
cd "00 - template"
pdflatex main.tex   # First pass — builds structure, writes .nav file
pdflatex main.tex   # Second pass — reads .nav, fixes total frame count in footer
```

### Cleanup auxiliary files after compilation

```bash
rm -f main.aux main.log main.nav main.out main.toc main.vrb main.snm main.fls main.fdb_latexmk main.synctex.gz
```

---

## Branch Protection

The `main` branch is protected. **All changes must go through a Pull Request.**
Direct pushes are blocked for non-admin contributors.

---

## Color Theme

The template uses the official **Facultad de Informática (UNLP)** bordeaux color:

| Token | Hex | Usage |
|---|---|---|
| `ColorUNLP` | `#8c0011` | Primary structure color (headers, blocks, footers) |

---

## Sponsors

| Category | Organization |
|---|---|
| Organiza | AAPC |
| Sede | UNLP — Facultad de Informática |
| Diamond Sponsor | GTS |
