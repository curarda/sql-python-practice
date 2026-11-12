# SQL & Python Practice

An interactive practice app for Python, pandas, and SQL, built from the table of contents of a
Turkish booklet, *"Veri Analisti Stajyeri için Python: Sıfırdan Uygulamalı Kitapçık"* ("Python
from Scratch for a Data Analyst Intern"). It follows the booklet's 20 chapters, from setup to
an end-to-end e-commerce case study. Each chapter starts with a short explanation, then
exercises follow. You write the code, run it, and get your answer checked with feedback.

**Live app (browser, installable on iPhone):** https://curarda.github.io/sql-python-practice/

The interface, exercises, and feedback are all in **Turkish** (the booklet's language);
full documentation is in [README.tr.md](README.tr.md).

## Who it is for

- Candidates preparing for a data analyst internship's Python/pandas/SQL technical test.
- Turkish-speaking beginners who want guided, auto-graded exercises with immediate feedback.

## What it does

- 20 chapters, ~70 exercises: Python basics, NumPy, pandas (reading, cleaning, groupby,
  merge, dates, stats), SQL, Excel, APIs/JSON, and a full e-commerce case study.
- All sample data is regenerated from the booklet's own seeded code, so results match the
  booklet's printed numbers exactly (net revenue, return rate, z-test, etc.).
- Code runs in your browser (Python via Pyodide: pandas, scipy, statsmodels), so nothing is
  sent to a server.
- Progress is saved in your browser only.
- Runs past 5 seconds are stopped so the page never freezes.

## Use on iPhone

1. Open the live link in **Safari**.
2. Tap Share → **Add to Home Screen**.

The first launch downloads the Python environment, which can take a few minutes. After that
it works offline.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The browser version is generated from `web/` and the root Python files into `docs/`; see the
developer section in [README.tr.md](README.tr.md).

## Tech

Python, pandas, NumPy, scipy, statsmodels, SQL (SQLite), Streamlit (local version), Pyodide
(browser version), pytest for tests (88 tests, run on Python 3.11, 3.14, and pandas 2.2.3).

Full documentation, the chapter list, and how to add new exercises: [README.tr.md](README.tr.md).
