# 🎬 Movie & OTT Platform Content Analysis

An end-to-end Data Science and Business Intelligence project comparing movie and television show catalogs across **Netflix**, **Amazon Prime Video**, **Disney+**, and **Hulu**. 

This repository implements the full Data Science Lifecycle: raw dataset extraction, cleaning, standardization, multi-catalog integration, descriptive statistical analysis, measures of central tendency and dispersion, and an interactive multi-page dashboard built with **Streamlit** and **Plotly**.

---

## 📌 Table of Contents
1. [Project Overview](#-project-overview)
2. [Technology Stack](#-technology-stack)
3. [Data Science Syllabus Alignment](#-data-science-syllabus-alignment)
4. [Dataset Architecture](#-dataset-architecture)
5. [Project Folder Structure](#-project-folder-structure)
6. [Data Pipeline & Preprocessing](#-data-pipeline--preprocessing)
7. [Exploratory Data Analysis (EDA) Findings](#-exploratory-data-analysis-eda-findings)
8. [Interactive Dashboard Features](#-interactive-dashboard-features)
9. [Installation & Setup](#-installation--setup)
10. [Streamlit Cloud Deployment](#-streamlit-cloud-deployment)

---

## 🎯 Project Overview

Streaming platforms (OTT) have fundamentally transformed global entertainment distribution. Each platform maintains distinct catalog strategies in content volume, runtime lengths, target audience demographics, regional origins, and exclusive vs. licensed catalogs.

This project delivers:
- **Unified Catalog of 22,998 titles** across 4 major streaming services.
- **Reproducible ELT Pipeline** (`src/preprocessing.py`) handling missing values, duration shifts, date parsing, and audience categorization.
- **Three Executed Jupyter Notebooks** with complete documentation, visualizations, and outputs.
- **High-Performance Multi-Page Streamlit Dashboard** with real-time responsive filters, Plotly visualizations, title searching, and CSV export.

---

## 🛠️ Technology Stack

| Layer | Tools / Libraries | Purpose |
|---|---|---|
| **Language** | Python 3.10+ | Core development |
| **Data Manipulation** | Pandas, NumPy | Data cleaning, reshaping, cross-platform aggregation |
| **Descriptive Statistics** | SciPy, NumPy, Pandas | Central tendency, dispersion, IQR, runtime metrics |
| **Data Visualization** | Plotly Express, Plotly Graph Objects, Matplotlib, Seaborn | Interactive charts, choropleth maps, treemaps |
| **Dashboard UI** | Streamlit | Responsive multi-page web application |
| **Notebooks** | Jupyter (`.ipynb`) | Reproducible analysis and academic documentation |
| **Storage** | Flat CSV files | Lightweight tabular persistence (no SQL DB required) |

---

## 🎓 Data Science Syllabus Alignment

This project directly demonstrates core university Data Science syllabus competencies:

- **Unit 1: Introduction to Data Science**
  - Data Science Lifecycle (Problem Definition → Acquisition → Cleaning → Integration → EDA → Communication).
  - Distinguishing predictive modeling from descriptive analytics.
- **Unit 2: Big Data & Structured Data**
  - Tabular CSV architecture, schemas, column dtypes, records, and memory optimization.
- **Unit 3: Statistics & Probability for Data Science**
  - Numerical vs categorical data classification.
  - Measures of Central Tendency (Mean, Median, Mode).
  - Measures of Dispersion (Standard Deviation, Variance, Min/Max Range, Interquartile Range).
  - Distribution shapes, skewness, and runtime frequencies.
- **Unit 6: Data Transformation & Data Integrity**
  - Data consistency validation across distinct sources.
  - Anomaly detection & resolution (shifted duration fields in rating columns).
  - Imputation and safe handling of missing values without fabricating data.
  - Categorical standardization (audience age certifications).
- **Unit 8: Data Engineering & ELT Processes**
  - Extract (4 raw CSVs) → Transform (clean, standardize, parse) → Load (`unified_ott_dataset.csv`).
  - Automated reusable Python preprocessing pipeline.
- **Unit 10: Visualization & Capstone Deployment**
  - Visual design principles, comparative charts, geographic maps, interactive dashboard deployment.

---

## 📁 Dataset Architecture

The analysis integrates four Kaggle OTT datasets:
1. **Netflix Movies and TV Shows**: 8,807 titles
2. **Amazon Prime Video Movies and TV Shows**: 9,668 titles
3. **Disney+ Movies and TV Shows**: 1,450 titles
4. **Hulu Movies and TV Shows**: 3,073 titles
- **Total Combined Records:** **22,998 titles** (22,041 unique titles, 718 multi-platform crossover titles).

### Unified Schema (`unified_ott_dataset.csv`):
```text
- show_id           : Original platform identifier
- title_id          : Globally unique composite ID (e.g. NFLX_s1, AMZN_s1)
- platform          : Platform name (Netflix, Amazon Prime, Disney+, Hulu)
- platform_code     : Platform ticker (NFLX, AMZN, DISN, HULU)
- type              : Content type ('Movie' or 'TV Show')
- title             : Standardized title string
- director          : Director(s) (Unknown if missing)
- cast              : Lead cast members (Unknown if missing)
- country           : Production country / territories (Unknown if missing)
- date_added        : Original date string added to catalog
- date_added_clean  : Parsed ISO timestamp (YYYY-MM-DD)
- year_added        : Year content was ingested to platform
- month_added       : Month content was ingested
- release_year      : Original release year of the movie or show
- rating            : Raw age rating (e.g. TV-MA, PG-13, 16+)
- rating_category   : Standardized target audience ('Kids', 'Teens', 'Adults', 'Unrated')
- duration          : Original runtime string (e.g. '90 min', '2 Seasons')
- duration_int      : Extracted numeric runtime integer
- duration_unit     : 'Minutes' or 'Seasons'
- duration_minutes  : Movie duration in minutes (numeric)
- duration_seasons  : TV Show duration in seasons (numeric)
- listed_in         : Full genre string
- primary_genre     : Lead genre category
- description       : Plot synopsis
```

---

## 📂 Project Folder Structure

```
movie-ott-content-analysis/
│
├── data/
│   ├── raw/
│   │   ├── netflix.csv
│   │   ├── amazon_prime.csv
│   │   ├── disney_plus.csv
│   │   └── hulu.csv
│   └── processed/
│       └── unified_ott_dataset.csv
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_exploratory_data_analysis.ipynb
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py          # Data ingestion, cleaning & ELT pipeline
│   ├── analysis.py               # Statistical computations & Plotly visualizations
│   └── generate_notebooks.py     # Reproducible notebook generator
│
├── dashboard/
│   ├── app.py                    # Page 1: Executive Overview (Dashboard Home)
│   ├── utils.py                  # Global filters, caching & UI styling
│   └── pages/
│       ├── 1_genre_analysis.py   # Page 2: Genre & Content Runtime Analysis
│       ├── 2_country_analysis.py # Page 3: Country Origins & Release Trends
│       └── 3_content_exploration.py # Page 4: Ratings & Interactive Catalog Explorer
│
├── requirements.txt              # Production Python dependencies
├── README.md                     # Project documentation
├── PROJECT_REPORT.md             # Formal academic capstone report
└── .gitignore
```

---

## ⚡ Data Pipeline & Preprocessing

Run the automated pipeline to transform raw datasets into the unified database:

```bash
python src/preprocessing.py
```

### Key Cleaning Operations Performed:
1. **Anomaly Correction**: Fixed 295 records (292 on Hulu, 3 on Netflix) where runtime values (e.g. `'74 min'`, `'2 Seasons'`) were mistakenly stored in the `rating` column while `duration` was `NaN`.
2. **Missing Value Imputation**: Missing values in `director`, `cast`, and `country` filled with `'Unknown'` to prevent artificial data fabrication.
3. **Audience Standardization**: Standardized fragmented platform ratings (e.g., `'13+'`, `'TV-14'`, `'PG-13'`, `'ALL'`) into 4 unified brackets:
   - **Kids**: `G`, `TV-G`, `TV-Y`, `TV-Y7`, `TV-Y7-FV`, `ALL`, `7+`
   - **Teens**: `PG`, `TV-PG`, `PG-13`, `TV-14`, `13+`, `16`, `16+`
   - **Adults**: `R`, `TV-MA`, `NC-17`, `18+`
   - **Unrated**: `NR`, `UR`, `NOT RATED`, `UNRATED`
4. **Runtime Decomposition**: Separated movie runtimes into integer minutes and TV series into integer seasons.

---

## 📊 Exploratory Data Analysis (EDA) Findings

The project delivers the 8 required core analyses:

1. **Content Distribution**:
   - Movies account for **71.4%** (16,419 titles); TV Shows account for **28.6%** (6,579 titles).
2. **Platform Comparison**:
   - Amazon Prime has the largest library (**9,668 titles**, 80.8% Movies).
   - Netflix has the second largest (**8,807 titles**, 69.6% Movies).
   - Hulu focuses heavily on TV shows (**53.7% TV Shows** vs 46.3% Movies).
   - Disney+ maintains a curated catalog (**1,450 titles**, 72.6% Movies).
3. **Genre Hierarchy**:
   - **Drama** (4,728) and **Comedy** (3,292) lead across all services.
   - Amazon Prime specializes in Action and Drama; Netflix in International Dramas and Stand-Up Comedy; Disney+ in Animation and Family.
4. **Geographic Distribution**:
   - Top 3 producing countries: **United States** (6,305), **India** (1,299), and **United Kingdom** (1,174).
5. **Release Trends**:
   - Exponential surge in OTT content releases starting in 2015, peaking between 2017 and 2021.
6. **Audience Demographics**:
   - **Teens / Young Adults** (45.4%) and **Adults** (30.8%) represent the bulk of catalogs.
   - Disney+ leads family content, with over 68% rated for Kids and Teens.
7. **Movie Runtime Dispersion**:
   - **Mean Duration:** 93.6 minutes | **Median:** 94.0 minutes | **Std Dev:** 35.7 minutes | **IQR:** 28.0 minutes.
   - Distribution is normal/bell-shaped with a peak around 90-100 minutes.
8. **TV Show Longevity**:
   - **64.2%** of TV shows conclude after 1 season (limited series or early cancellations).
   - Only **35.8%** achieve multi-season renewals.

---

## 🖥️ Interactive Dashboard Features

The Streamlit dashboard (`dashboard/app.py`) provides 4 curated, publication-grade analytical pages:

- **Page 1: Executive Overview (`app.py`)**
  - KPI metric cards: Total Titles (22,998), Movies (71.4%), TV Shows (28.6%), Active Services (4), Unique Titles (22,041).
  - Platform catalog size & format breakdown (grouped bar chart).
  - Multi-decade content release trajectory (historical velocity).
  - Platform summary matrix with exact counts and format proportions.
- **Page 2: Genre & Runtime Dynamics (`1_genre_analysis.py`)**
  - Interactive Top N genre slider (5 to 20 categories).
  - Ranked horizontal bar chart of top genres.
  - Stacked platform comparison across top content genres.
  - Measures of central tendency and dispersion for movie durations (Sample size, Mean, Median, Std Dev, IQR, Min-Max).
  - Tukey's box plots displaying duration quartiles and outliers by platform.
  - Runtime frequency distribution histogram.
  - TV show season distribution and renewal longevity metrics (Single-season vs Multi-season).
- **Page 3: Geographic Footprint & Release Trajectories (`2_country_analysis.py`)**
  - Global choropleth map of production output worldwide.
  - Top 10 content-producing countries ranked horizontal bar chart.
  - Platform breakdown matrix across top 8 content-producing countries.
  - Content release velocity over time (Movies vs TV Shows vs Total).
  - Annual release volume trajectories by platform (1920–Present).
- **Page 4: Catalog Overlap & Content Explorer (`3_content_exploration.py`)**
  - Target audience age certification distribution (Kids, Teens, Adults, Unrated) across platforms.
  - Multi-platform licensing overlap heatmap (pairwise shared titles).
  - Shared title matrix with quick-filtering presets (e.g., Netflix & Prime Video, 3+ services).
  - Searchable catalog browser with instant keyword filtering (title, director, cast, genre).
  - **Download filtered data as CSV** button.
  - Deep title metadata inspector with complete record diagnostics across platforms.

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14
- Virtual environment (recommended)



### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the data pipeline (generates unified dataset)
```bash
python src/preprocessing.py
```

### 3. Launch the Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```
Open your browser at `http://localhost:8501`.

### 4. Run Jupyter Notebooks
```bash
jupyter notebook notebooks/
```

---

## 🌐 Streamlit Cloud Deployment

1. Push your repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io/).
3. Connect your GitHub account and select your repository.
4. Set the main file path to:
   ```text
   dashboard/app.py
   ```
5. Click **Deploy**!

