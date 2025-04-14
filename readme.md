Below is a complete `README.md` file that you can copy and paste directly into your project:

---

```markdown
# Text Summarization Project

This project demonstrates a complete data pipeline for automated text summarization. The application scrapes news articles from Inshorts across multiple categories (Technology, Sports, and World), preprocesses and normalizes the collected text, and then generates a frequency-based extractive summary. The summarized data is output to a CSV file for further analysis or sharing.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [License](#license)

## Overview

The Text Summarization Project is designed to illustrate the process of turning raw news data into concise summaries. The process includes:

1. **Web Scraping:** Extracting headlines and article content from Inshorts.
2. **Text Preprocessing:** Cleaning the text by removing HTML tags, accented characters, extra spaces, and expanding contractions.
3. **Normalization:** Converting text to lowercase, lemmatizing words, and removing special characters and stopwords.
4. **Extractive Summarization:** Identifying key sentences by calculating a frequency-based score.
5. **Output Generation:** Saving the processed data and summaries into a CSV file.

## Features

- **Automated Web Scraping:** Collects news from multiple categories via predefined URLs.
- **Preprocessing Pipeline:** Utilizes BeautifulSoup, NLTK, and spaCy for thorough text cleaning and normalization.
- **Extractive Summarization:** Implements a frequency-based algorithm to extract the most important sentences as a summary.
- **CSV Export:** Facilitates further analysis by exporting the results to a CSV file.
- **Modular Code:** The project is organized into reusable functions for each step of the pipeline.

## Project Structure

```plaintext
├── streamlit.py             # (Optional) Streamlit-based app for interactive summarization
├── test_NLP_IA-2.py         # Main script: Scrapes data, preprocesses text, generates summaries, and saves output
├── news_with_summary.csv    # Output CSV file containing news data and generated summaries
└── README.md                # This file
```

> **Note:** The project is modular in design, making it easy to modify or extend individual steps such as scraping, preprocessing, or the summarization algorithm.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/text-summarization-project.git
    cd text-summarization-project
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv env
    source env/bin/activate     # On Windows use: env\Scripts\activate
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Download the spaCy English model:**
    ```bash
    python -m spacy download en_core_web_sm
    ```

> **requirements.txt:**  
> Ensure your `requirements.txt` includes the following packages:
> - `requests`
> - `beautifulsoup4`
> - `pandas`
> - `numpy`
> - `matplotlib`
> - `seaborn`
> - `nltk`
> - `spacy`

## Usage

To run the text summarization pipeline, execute the main script:

```bash
python test_NLP_IA-2.py
```

If you want to try the interactive version (if available), you can launch the Streamlit app with:

```bash
streamlit run streamlit.py
```

These scripts will:
- Scrape news articles from the Inshorts website.
- Clean and normalize the text.
- Generate a frequency-based extractive summary for each article.
- Save the detailed results along with summaries in `news_with_summary.csv`.

## How It Works

1. **Data Collection:**  
   The `build_dataset` function retrieves news articles by scraping headlines and article bodies from the specified Inshorts URLs.

2. **Text Preprocessing & Normalization:**  
   The preprocessing pipeline includes:
   - **HTML Stripping:** Removing HTML tags from the text.
   - **Accent Removal:** Converting accented characters to plain ASCII.
   - **Contraction Expansion:** Expanding shortened forms (e.g., "can't" to "cannot").
   - **Lowercasing:** Standardizing text to lowercase.
   - **Lemmatization:** Using spaCy to reduce words to their base forms.
   - **Special Character & Stopword Removal:** Eliminating non-alphanumeric characters and common stopwords using NLTK.

3. **Extractive Summarization:**  
   The summarizer:
   - **Tokenizes sentences:** Splitting articles into individual sentences.
   - **Builds a frequency table:** Counting occurrences of words (ignoring stopwords).
   - **Scores sentences:** Assigning each sentence a score based on the average frequency of its words.
   - **Generates the summary:** Selecting the top sentences as a summary based on a defined reduction ratio (e.g., 30%).

4. **Output:**  
   After processing, the project outputs:
   - The cleaned full text.
   - A summarized version of the article.
   - Metrics such as word counts and compression percentage.
   - A CSV file (`news_with_summary.csv`) containing all the data.

## Requirements

- **Python 3**  
- **Libraries:**
  - requests
  - beautifulsoup4
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - nltk
  - spacy
- **Additional Resources:**
  - NLTK resources: `stopwords` and `punkt`
  - spaCy's `en_core_web_sm` language model

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this code as per the license terms. Attribution is appreciated.

```

---

Feel free to modify the text to better suit your project's specifics (such as repository URLs, additional features, or updated instructions).