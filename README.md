# IPL Data Analyzer

My first full data analysis project — an interactive dashboard that digs into 17 seasons of IPL cricket (2008–2024), from team performance to individual player stats, built entirely with Python and SQL.

## Live App
 [Check it out here](https://ipl-analyser-bghvgiemmtey2zrercnf4w.streamlit.app/)

## Why I built this

I wanted a project that would actually teach me the full data workflow — not just another notebook with a few plots, but something that goes from raw, messy data all the way to a deployed, interactive app. IPL felt like the perfect dataset: it's something I actually enjoy watching, and it's big enough (260,000+ ball-by-ball records across 1,000+ matches) to force me to think about performance and clean code, not just quick hacks.

## What it does

- **Team Analysis** — win percentages, toss-decision impact on match outcomes, most successful venues
- **Batsman Analysis** — top run-scorers, six-hitters, and a searchable player-stats lookup (runs, strike rate, fours/sixes)
- **Bowler Analysis** — top wicket-takers, most economical bowlers, individual bowler stats
- **Season Analysis** — champions by season, a heatmap of team wins across all 17 years
- **SQL Explorer** — run predefined queries or write your own custom SQL directly against the dataset

## Tech Stack

`Python` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `SQLite` · `Streamlit`

## Project Structure
## Project Structure

```text
IPL-ANALYSER/
│
├── Data/
│   ├── Raw/
│   │   ├── matches.csv
│   │   └── deliveries.csv
│   │
│   └── Processed/
│       ├── matches_clean.csv
│       ├── deliveries_clean.csv
│       └── ipl.db
│
├── Notebooks/
│   └── 01_data_cleaning.ipynb
│
├── sql/
│   └── queries.sql
│
├── src/
│   ├── data_loader.py
│   ├── db_utils.py
│   ├── visuals.py
│   └── analysis.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## A bug I actually learned a lot from

While cleaning the ball-by-ball data, I filled missing `dismissal_kind` values with the string `"None"` and saved it to CSV. When I reloaded that file later, pandas silently converted the text `"None"` back into an actual `NaN` — turns out that's one of pandas' default "null" keywords. That broke a filter I had (`!= 'None'`), which ended up inflating wicket counts by roughly 20x (one bowler showed 4,600+ career wickets, which is obviously impossible). 

Fixed it by keeping those columns as real `NaN` instead of a string placeholder, and using `.notna()` in pandas / `IS NOT NULL` in SQL instead. Small bug, but it taught me to actually double-check my numbers against reality instead of assuming the code "ran without errors" means it's correct.

## Dataset

[IPL Complete Dataset (2008–2024) — Kaggle](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)
