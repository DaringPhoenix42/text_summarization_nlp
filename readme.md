Below is an **enhanced** version of your README that keeps the same sections and flow but refines the language, structure, and clarity. Feel free to tailor it further to your needs!

---

```markdown
# Text Summarization Project

This repository demonstrates a complete data pipeline for **automated text summarization**. It scrapes news articles from [Inshorts](https://inshorts.com) across multiple categories (Technology, Sports, and World), preprocesses and normalizes the text, and then generates frequency-based summaries. The final output is written to a CSV file for easy sharing or analysis.

---

# Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Project Structure](#project-structure)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [How It Works](#how-it-works)  
7. [Requirements](#requirements)  
8. [License](#license)  

---

## Overview

The **Text Summarization Project** converts large volumes of news data into concise summaries. Key steps in the workflow include:

1. **Web Scraping** – Gathering headlines and article text from Inshorts.  
2. **Text Preprocessing** – Cleaning and standardizing the text by removing HTML tags, accented characters, extra spaces, and contractions.  
3. **Normalization** – Lowercasing and lemmatizing text, as well as removing special characters and stopwords.  
4. **Frequency-Based Summarization** – Scoring sentences based on word frequencies to identify the most important content.  
5. **CSV Output** – Storing the final summaries alongside metadata (category, headline, etc.) for future reference.

---

## Features

- **Automated Web Scraping** – Collects articles from predefined Inshorts categories.
- **Robust Preprocessing** – Uses BeautifulSoup, NLTK, and spaCy for thorough text cleaning, normalization, and lemmatization.
- **Extractive Summarization** – Employs a frequency-based algorithm to pick out the most relevant sentences from each article.
- **CSV Export** – Summaries and associated article data are saved to `news_with_summary.csv`.
- **Modular Codebase** – Functions are organized to be easily maintained or enhanced, e.g., adding custom summarization methods or new data sources.

---

## Project Structure

```
├── streamlit_app.py        # Optional Streamlit-based UI for interactive exploration
├── test_NLP_IA-2.py        # Main script with web scraping, text preprocessing, summarization, and CSV export
├── news_with_summary.csv   # Automatically generated CSV with summarized content
└── README.md               # Project documentation (this file)
```

> **Note:** The project is modular, allowing you to adapt individual components (like adding new data sources or swapping in advanced summarization algorithms) with minimal effort.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/text-summarization-project.git
   cd text-summarization-project
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate     # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the spaCy English language model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

> **requirements.txt** should include:
> - `requests`  
> - `beautifulsoup4`  
> - `pandas`  
> - `numpy`  
> - `matplotlib`  
> - `seaborn`  
> - `nltk`  
> - `spacy`  

---

## Usage

1. **Run the main script**:
   ```bash
   python test_NLP_IA-2.py
   ```
   This script:
   - Scrapes news articles from Inshorts.  
   - Cleans and normalizes the text.  
   - Summarizes content using a frequency-based approach.  
   - Saves the summarized data in `news_with_summary.csv`.

2. **(Optional) Launch the Streamlit UI** (if available):
   ```bash
   streamlit run streamlit_app.py
   ```
   This opens a web-based dashboard where you can view the scraped articles, summaries, and other details.

---

## How It Works

1. **Data Collection**  
   - `build_dataset` fetches data from Inshorts URLs, extracting headlines (`<span itemprop="headline">`) and articles (`<div itemprop="articleBody">`).

2. **Text Preprocessing & Normalization**  
   - **Strip HTML Tags** using BeautifulSoup.  
   - **Remove Accents** and special characters for consistency.  
   - **Expand Contractions** (e.g., "don't" → "do not").  
   - **Lowercase & Lemmatize** words with spaCy.  
   - **Stopword Removal** using NLTK to enhance summarization results.

3. **Extractive Summarization**  
   - **Sentence Splitting** – Break the article into individual sentences.  
   - **Frequency Table** – Calculate how often each word appears, ignoring stopwords.  
   - **Sentence Scoring** – Assign each sentence a score based on the sum of word frequencies.  
   - **Summary Selection** – Extract the top N sentences (determined by a user-defined ratio).

4. **Output**  
   - **Dataframe** with headlines, articles, cleaned text, and summaries.  
   - **CSV File** (`news_with_summary.csv`) containing all relevant fields for easy analysis or reuse.

---

## Requirements

- **Python 3.7+** (recommended)  
- **Libraries**:
  - requests  
  - beautifulsoup4  
  - pandas  
  - numpy  
  - matplotlib  
  - seaborn  
  - nltk  
  - spacy  
- **Additional**:
  - NLTK corpus downloads: `stopwords` and `punkt`  
  - spaCy model: `en_core_web_sm`  

---


