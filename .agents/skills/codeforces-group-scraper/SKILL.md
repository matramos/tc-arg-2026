---
name: codeforces-group-scraper
description: Scrapes all contests and submissions from a private or public Codeforces group and analyzes them to output LaTeX slide snippets.
---

# Codeforces Group Scraper Skill

Use this skill to scrape all contests and submissions from a Codeforces Group and automatically generate statistics slides (LaTeX code) for Training Camp presentations.

---

## 1. Authentication Requirements

Since Codeforces groups are private or require browser authentication, the scraper runs locally using your active session cookies.

### How to Retrieve Cookies:
1. Log into [Codeforces](https://codeforces.com) in your browser.
2. Open Developer Tools (`F12` or `Ctrl+Shift+I`).
3. Navigate to the **Application** tab (or **Storage** in Firefox) and select **Cookies** -> `https://codeforces.com`.
4. Copy the values of the following cookies:
   * **`JSESSIONID`**: The Java session identifier.
   * **`39ceb`**: Codeforces session tracking cookie.

---

## 2. Scraping Submissions

The `scrape.py` script queries the contests page of the group, discovers all contests, and then scrapes every submission page-by-page.

### Command Syntax:
```bash
python3 .agents/skills/codeforces-group-scraper/scripts/scrape.py \
    --group "YOUR_GROUP_ID" \
    --jsessionid "JSESSIONID_VALUE" \
    --cookie-39ceb "39CEB_VALUE" \
    --output "submissions.json"
```

* **`YOUR_GROUP_ID`**: The alphanumeric ID of the group in the URL (e.g., `GHvtTrfZFd` for `https://codeforces.com/group/GHvtTrfZFd`).
* **`submissions.json`**: The destination path where the scraped raw data will be saved.

*Note: The script includes a rate-limiting delay between requests to be polite to Codeforces servers.*

---

## 3. Analyzing & Generating LaTeX Slides

The `analyze.py` script processes the scraped `submissions.json` file and outputs the fully formatted LaTeX code blocks for the Training Camp closing presentation slides:

* **Estadísticas del Training Camp** (totals and averages).
* **Submissions por Día - Gráfico** (TikZ bar chart scaled dynamically).
* **Análisis de Submissions** (TikZ pie charts for languages and judge verdicts).
* **Estadísticas Adicionales** (participation and performance metrics).
* **Total de Submissions** (grand summary).

### Command Syntax:
```bash
python3 .agents/skills/codeforces-group-scraper/scripts/analyze.py submissions.json
```

---

## 4. Dependencies

* **No third-party dependencies required!** Both scripts run using standard Python library modules (`urllib.request`, `html.parser`, `json`, `re`, `argparse`, `time`, etc.).
* Requires Python 3.6+.
