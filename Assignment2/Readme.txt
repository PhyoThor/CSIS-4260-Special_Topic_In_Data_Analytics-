# NVIDIA Financial Text Analysis Project

This repository contains the full pipeline for scraping, analyzing, and visualizing financial discussions related to NVIDIA from Reddit and CNN news.

---

## 📦 Project Structure

```
Assignment2/
├── 1.A_scrape_praw.py
├── 1.B_scrape_bs4.py
├── 2.A_Topic_Modeling.py
├── 2.B_KeyBERT.py
├── 2.C_OpenAI.py
├── 3.A_Visualise_Reddit.py
├── 3.B_Visualise_CNN.py
├── 3.C_Correlation_Analysis.py
├── 3.D_Topic_Insight_dashboard.py
├── 4.GPT_Score_Heatmap_by_Topic.py
├── data/
│   ├── nvidia_praw_clean.csv
│   ├── nvidia_cnn_bing_clean.csv
│   ├── nvidia_praw_enriched.csv
│   ├── nvidia_cnn_bing_enriched.csv
│   ├── reddit_topic_labels.csv
│   ├── cnn_topic_labels.csv
├── visuals/
│   ├── reddit_score_histogram.png
│   ├── cnn_wordcloud.png
│   ├── heatmap_topic_vs_score.png
└── README.md
```

---

## 🛠 Installation

```bash
git clone https://github.com/your-username/NVIDIA-Text-Analysis.git
cd NVIDIA-Text-Analysis
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 📚 Required Libraries

- `praw`
- `beautifulsoup4`
- `requests`
- `pandas`
- `matplotlib`
- `seaborn`
- `wordcloud`
- `gensim`
- `openai`
- `keybert`
- `scikit-learn`

Install them via:

```bash
pip install -r requirements.txt
```

---

## 🧠 Sample Code Usage

### Run topic modeling

```bash
python 2.A_Topic_Modeling.py
```

### Generate GPT summaries

```bash
python 2.C_OpenAI.py
```

### Create visual reports

```bash
python 3.A_Visualise_Reddit.py
python 3.B_Visualise_CNN.py
python 4.GPT_Score_Heatmap_by_Topic.py
```

---

## 📈 Analysis Output

- Topic modeling with Gensim LDA
- Keyword extraction using KeyBERT
- GPT-3.5 summary generation with directional scores
- Bar charts, word clouds, and heatmaps
- Final output: academic-style report + presentation

---

## 🧠 Author Notes

- Ideal for financial analytics learners, NLP projects, or real-time investor sentiment tracking.
- Designed to be modular — easily extendable for other companies or domains.
