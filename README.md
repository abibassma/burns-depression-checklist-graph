<!-- TOC --><a name="burns-depression-checklist-graph"></a>
# Burns Depression Checklist Graph

## Table of Content
<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

   * [🚨 Content Warning (CW)](#-content-warning-cw)
   * [⚠️ Disclaimer / Privacy](#-disclaimer)
   * [Description](#description)
   * [Background](#background)
      + [Burns Depression Checklist (BDC)](#burns-depression-checklist-bdc)
      + [Instructions](#instructions)
      + [What are the scores computed?](#what-are-the-scores-computed)
      + [Interpretation](#interpretation)
   * [Guide](#guide)
      + [Repo structure](#repo-structure)
      + [CSV format](#csv-format)
      + [Features](#features)
   * [Usage](#usage)
   * [Configuration](#configuration)
   * [Troubleshooting](#troubleshooting)
   * [Notes about Google Forms / Sheets](#notes-about-google-forms-sheets)
   * [To-Do](#to-do)
   * [Thank you 💖](#thank-you-)
   * [ChangeLog](#changelog)
   * [⚖️ MIT License](#-mit-license)

<!-- TOC end -->



<!-- TOC --><a name="-content-warning-cw"></a>
## 🚨 Content Warning (CW)

This project contains references to **depression** and **suicidal ideation**. If you may be affected by this content, please take care; seek support if needed.

**If you feel like you may harm yourself, *please*, please call a crisis hotline.**
https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines

<!-- TOC --><a name="-disclaimer"></a>
## ⚠️ Disclaimer / Privacy

This tool is for educational purposes, personal tracking and visualization only; it is **not** a clinical diagnostic tool. Please consult a mental health professional rather than a random internet person like me.

All user data (CSV files) remain local to your machine unless you choose to upload or commit them. **(Do not commit personal data (CSV ) to public repositories.)**

_If you share outputs (HTML/PNG), remove or redact identifying details first (like timestamps)._

This project does not send your data anywhere; any external integrations (e.g., Google Sheets export) are optional. Review those services' privacy policies before use.


<!-- TOC --><a name="description"></a>
## Description

Plot interactive time-accurate graphs of the Burns Depression Checklist (BDC) and a weighted suicidal-ideation score from CSV data using Python and Plotly.

This project reads a CSV with timestamps and scores, computes a weighted Score (Score × 8), and generates interactive Plotly graphs. Points are placed at their exact timestamps so irregular spacing between dates is preserved. The project adds shaded bands for depression levels (see Backgroud/Interpretation), marks invalid/out-of-range points, and provides toggle controls.

Useful for visualizing mood evolution recorded via forms or journals. The interactive HTML output lets you inspect exact dates and values.

<!-- TOC --><a name="background"></a>
## Background

<!-- TOC --><a name="burns-depression-checklist-bdc"></a>
### Burns Depression Checklist (BDC)

*Burns Depression Checklist* table (2–1, page 20) from the book: **Feeling Good: the new mood therapy** by David D. Burns*, is a single-page assessment comprised of 25 questions and a 0-4 rubric so that test-takers can rate their own depression symptoms.

**Copyright © 1984 by David D. Burns, M.D. (Revised, 1996.)*

<!-- TOC --><a name="instructions"></a>
### Instructions

Indicate how much you have experienced each symptom **during the past week**, including today.

_Please answer all 25 items._
* 0: Not at all
* 1: Somewhat
* 2: Moderately
* 3: A lot
* 4: Extremely


<!-- TOC --><a name="what-are-the-scores-computed"></a>
### What are the scores computed?

* _BDC Score_: the Burns Depression Checklist total score as recorded in the "BDC Score" column, the total sum of all your question entries. (from 0-100)

* _Score_ (or Sui-score/Suicidal Ideation score): the total sum of the final three questions. (from 0-12)
Specifically:
    * Question n°23: Do you have any suicidal thoughts?
    * Question n°24: Would you like to end your life?
    * Question n°25: Do you have a plan for harming yourself?

**If you are experiencing suicidal thoughts or severe distress, seek immediate professional help**
<!-- TOC --><a name="interpretation"></a>
### Interpretation

(This is what the horizental bands are based on.)

| BDC SCORE  | Interpretation |
| ------------- |:-------------:|
| 0-5     | No depression    |
| 6-10      | Normal but unhappy    |
| 11-25     | Mild depression    |
|26-50|Moderate depression|
|51-75|Severe depression|
|76-100|Extreme depression|


<!-- TOC --><a name="guide"></a>
## Guide

<!-- TOC --><a name="repo-structure"></a>
### Repo structure


* data/ *raw CSV file **(⚠️ do NOT commit personal data!)***
* outputs/ *— generated HTML figures*
* src/
    * main.py — plotting script
* README.md
* requirements.txt


<!-- TOC --><a name="csv-format"></a>
### CSV format

Expected CSV header (example):

    Horodateur,Score,BDC Score,Sui-score (multip.)
    03/01/2025 06:30:21,0,24,0

Format:

    Horodateur: timestamp (default parsed as dd/mm/YYYY HH:MM:SS)
    Score: numeric (used for weighted suicidal-ideation score)
    BDC Score: numeric

If your timestamp uses mm/dd order, set DAYFIRST = False in src/main.py.

(From more details, see above Backgroud/What are the scores computed?)

<!-- TOC --><a name="features"></a>
### Features

* Parses timestamps and preserves true time spacing on the x-axis.

* Computes weighted suicidal ideation score (based on the last three questions of the self-assesment): **Score × SCORE_WEIGHT** (configurable; default 8).
> Picked 8 as multiplier because 12 is max for sui-score and 100 for BDC and the division roughly gives 8.3

* Two interactive outputs:
    * px.line figure (simple)
    * go.Figure with shaded horizontal bands for depression levels and toggle buttons

* Shaded bands: No depression, Normal but unhappy, Mild, Moderate, Severe, Extreme.

* Invalid-value handling:

        Rows with Score_weighted or BDC Score outside 0–100 are excluded from main series.
        Invalid points are shown as a separate marker trace (legend-only by default) and logged to console.

* Saves interactive HTML to outputs/

<!-- TOC --><a name="usage"></a>
## Usage

* Place your CSV in data/ (example: data/data.csv). **Do not commit sensitive info.**
* Install dependencies: pip install -r requirements.txt
* Run: python src/main.py
    * outputs/fig_px_line.html
    * outputs/fig_go_line.html

<!-- TOC --><a name="configuration"></a>
## Configuration

You may edit src/main.py variables:

    CSV_PATH : path to your CSV (default "data.csv")
    OUTPUT_DIR : where outputs are saved (default "outputs")
    SCORE_WEIGHT : multiplier for Score => Score_weighted (default 8)
    DAYFIRST : True if timestamps are dd/mm/YYYY (default True)

<!-- TOC --><a name="troubleshooting"></a>
## Troubleshooting

If you get NaNs or no output:

* Check printed debug output in the console (the script prints raw columns, dtypes, and rows with parse issues).
* Verify column names exactly match: Horodateur, Score, BDC Score (case-sensitive).
* Ensure timestamps parse correctly; adjust DAYFIRST or timestamp format.

<!-- TOC --><a name="notes-about-google-forms-sheets"></a>
## Notes about Google Forms / Sheets

I originally used a Google Form + Google Spreadsheet (inspired by Feeling Good) to track mood weekly over the years. Google Sheets’ built-in charting treats points as evenly spaced, so _irregular_ timestamps appear visually misleading (e.g., days and weeks look equally spaced).

![Image displaying difference between Google Spreadsheet and Python graphs for same data-points (spaced by one day)](https://file.garden/aN12BxVtC3JhzCRB/github/bdc/bdc_image_example_problem.PNG)

_Image displaying difference between Google Spreadsheet graph (on the left) and Python graph (on the right) for same data-points (spaced by one day)._

That limitation motivated this project; exporting CSV and plotting with Python/Plotly preserves true time spacing... and not only that! It gives interactive inspection of exact dates and points. (So I can see my journal entry for that day for example), and I can _see_ (thanks to the colored bands) what depression ranges we're in _at a glance_ without having to squint and do mental-math. :3


<!-- TOC --><a name="to-do"></a>
## To-Do
(Don't expect regular updates, lmao. I hope I have time)
* Add a Google Form template for the Burns Depression Checklist and instructions to clone it.
* Add instructions for connecting the Google Form to a Google Spreadsheet and exporting to CSV automatically (or via Apps Script).
* Add an option to fetch CSV directly from Google Sheets (authenticated flow or published CSV link).
* Improve UI: per-band toggles, export PNG/PDF, date-range filtering, smoothing options.
* Translate this project so it can reach out more people? (in French/Moroccan Darija/Arabic)
* Ditch the Google Form and make a static website that can export CSV and add data to it after filling the self-assessment?

<!-- TOC --><a name="thank-you-"></a>
## Thank you 💖
Yes, you! Thank you, whoever you are. You are enough, always! Good luck. 🦈

<!-- TOC --><a name="changelog"></a>
## ChangeLog

15/04/2026: Added an item to the To-Do list and wording in Read.md
14/04/2026: Initial release: CSV parsing, weighted-score computation, interactive Plotly graphs with time-accurate x-axis, shaded depression-level bands, invalid-value handling, and HTML outputs. Added Read.md.

<!-- TOC --><a name="-mit-license"></a>
## ⚖️ MIT License

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

