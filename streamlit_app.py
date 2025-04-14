

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
import spacy
import os
import warnings

# (Optional) Suppress Torch watcher warning if desired
warnings.filterwarnings("ignore", message="Tried to instantiate class '__path__._path'")

# ===================== Page Config =====================
st.set_page_config(
    page_title="News Summarization App",
    layout="wide",  # Maximize horizontal space
)

# ===================== Download NLTK Resources =====================
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords

stopword_list = stopwords.words('english')
if 'no' in stopword_list:
    stopword_list.remove('no')
if 'not' in stopword_list:
    stopword_list.remove('not')

tokenizer = ToktokTokenizer()
nlp = spacy.load('en_core_web_sm')

# ===================== Define Contraction Map =====================
CONTRACTION_MAP = {
    "can't": "cannot",
    "won't": "will not",
    "n't": " not",
    "i'm": "i am",
    "it's": "it is",
    # Add more contractions as needed...
}

# ===================== Data Pipeline Functions =====================

# --------- Step 3: Build Dataset from Inshorts ---------
seed_urls = [
    'https://inshorts.com/en/read/technology',
    'https://inshorts.com/en/read/sports',
    'https://inshorts.com/en/read/world'
]

def build_dataset(seed_urls):
    news_data = []
    for url in seed_urls:
        st.info(f"Scraping from: {url}")
        news_category = url.split('/')[-1]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.find_all('span', itemprop='headline')
        articles = soup.find_all('div', itemprop='articleBody')
        st.success(f"Found {len(headlines)} headlines and {len(articles)} articles in '{news_category}' category")
        for headline, article in zip(headlines, articles):
            news_data.append({
                'news_headline': headline.get_text(strip=True),
                'news_article': article.get_text(strip=True),
                'news_category': news_category
            })
    if not news_data:
        st.error("No articles were scraped. The website structure might have changed.")
    else:
        st.success(f"Total articles collected: {len(news_data)}")
    return pd.DataFrame(news_data)

# --------- Step 4: Text Preprocessing & Normalization ---------
def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_accented_chars(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    # Build regex for matching contractions
    contractions_pattern = re.compile(
        '({})'.format('|'.join(re.escape(key) for key in contraction_mapping.keys())),
        flags=re.IGNORECASE | re.DOTALL
    )
    
    def expand_match(contraction):
        match = contraction.group(0)
        expanded = contraction_mapping.get(match.lower())
        return expanded if expanded else match

    expanded_text = contractions_pattern.sub(expand_match, text)
    return re.sub("'", "", expanded_text)

def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-Z0-9\s]' if not remove_digits else r'[^a-zA-Z\s]'
    return re.sub(pattern, '', text)

def lemmatize_text(text):
    doc = nlp(text)
    return ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in doc])

def remove_stopwords(text, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    return ' '.join(filtered_tokens)

def normalize_corpus(
    corpus, 
    html_stripping=True,
    contraction_expansion=True,
    accented_char_removal=True,
    text_lower_case=True,
    text_lemmatization=True,
    special_char_removal=True,
    stopword_removal=True,
    remove_digits=True
):
    normalized_corpus = []
    for doc in corpus:
        if html_stripping:
            doc = strip_html_tags(doc)
        if accented_char_removal:
            doc = remove_accented_chars(doc)
        if contraction_expansion:
            doc = expand_contractions(doc)
        if text_lower_case:
            doc = doc.lower()

        # Remove newlines, etc.
        doc = re.sub(r'[\r|\n|\r\n]+', ' ', doc)

        if text_lemmatization:
            doc = lemmatize_text(doc)

        if special_char_removal:
            special_char_pattern = re.compile(r'([{.(-)!}])')
            doc = special_char_pattern.sub(" \\1 ", doc)
            doc = remove_special_characters(doc, remove_digits=remove_digits)

        # Remove extra whitespace
        doc = re.sub(' +', ' ', doc)

        if stopword_removal:
            doc = remove_stopwords(doc, is_lower_case=text_lower_case)

        normalized_corpus.append(doc)
    return normalized_corpus

# --------- Step 5: Frequency-Based Extractive Summarization ---------
def split_sentences(text):
    return sent_tokenize(text)

def split_words(text):
    return word_tokenize(text.lower())

def build_frequency_table(text, stopwords):
    words = split_words(text)
    freq_table = {}
    for word in words:
        if word in stopwords:
            continue
        freq_table[word] = freq_table.get(word, 0) + 1
    return freq_table

def score_sentences(sentences, freq_table):
    sentence_scores = {}
    for sentence in sentences:
        sentence_words = split_words(sentence)
        if len(sentence_words) == 0:
            continue
        score = sum(freq_table.get(word, 0) for word in sentence_words)
        sentence_scores[sentence] = score / len(sentence_words)
    return sentence_scores

def generate_summary(text, stopwords, reduction_ratio=0.3):
    sentences = split_sentences(text)
    if len(sentences) == 0:
        return ""
    freq_table = build_frequency_table(text, stopwords)
    sentence_scores = score_sentences(sentences, freq_table)
    summary_length = max(1, int(len(sentences) * reduction_ratio))
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:summary_length]
    summary = ' '.join([sentence for sentence in sentences if sentence in top_sentences])
    return summary

# ===================== Helper Functions for Theming =====================
def load_css(theme_choice):
    """
    Dynamically load CSS based on user theme selection: "Light" or "Dark".
    """
    if theme_choice == "Dark":
        st.markdown(
            """
            <style>
            /* Dark theme background */
            .main {
                background-color: #1e1e1e !important;
                color: #ffffff !important;
            }
            /* Override text color for various elements */
            body, .css-17z2v0h, .css-1cpxqw2, .css-1d391kg, .css-7snfe4, .st-cx {
                color: #ffffff !important;
            }
            /* Sidebar styling */
            .css-1d391kg {
                background-color: #2e2e2e !important;
            }
            /* Button styling */
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 0.5em 1em;
                font-size: 1em;
                margin: 0.2em;
                border-radius: 8px;
            }
            /* Dataframe styling */
            .dataframe {
                background-color: #333333;
                color: #ffffff;
            }
            /* Headers, subheaders, etc. */
            h1, h2, h3, h4 {
                color: #ffffff !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        # Light theme
        st.markdown(
            """
            <style>
            /* Light theme background */
            .main {
                background-color: #f9f9f9 !important;
                color: #000000 !important;
            }
            /* Override text color for various elements */
            .css-1d391kg, .css-1cpxqw2 {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            .css-17z2v0h, .st-cx {
                color: #000000 !important;
            }
            /* Button styling */
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 0.5em 1em;
                font-size: 1em;
                margin: 0.2em;
                border-radius: 8px;
            }
            /* Headers, subheaders, etc. */
            h1, h2, h3, h4 {
                color: #000000 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

def add_header():
    """
    Render a custom header at the top of the page.
    """
    st.markdown(
        """
        <div style='text-align: center; padding: 15px; background-color: #4CAF50; 
                    color: white; border-radius: 8px; margin-bottom: 20px;'>
            <h2 style="margin: 0;">📰 News Summarization App</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

def add_footer():
    """
    Render a custom footer at the bottom of the page.
    """
    st.markdown(
        """
        <hr style='margin-top: 50px;'>
        <p style='text-align:center'>
            Made with <span style='color:red;'>&#10084;</span> using Streamlit
        </p>
        """,
        unsafe_allow_html=True
    )

# ===================== Main App Layout =====================

# Sidebar Theme Selection
theme_choice = st.sidebar.selectbox("Theme Mode", ["Light", "Dark"], index=0)

# Load the selected theme CSS
load_css(theme_choice)

# Add a custom header
add_header()

st.markdown(
    """
    Welcome to this **News Summarization App**.  
    It scrapes the latest news from Inshorts (Technology, Sports, and World categories), 
    cleans and normalizes the text, generates a frequency-based extractive summary, 
    and displays the summarized data below.
    """,
    help="Use the sidebar to switch between Light or Dark theme."
)

st.sidebar.header("Configuration")
reduction_ratio = st.sidebar.slider("Summary Reduction Ratio", 0.1, 0.5, 0.3, 0.1)

# Button to scrape and process
if st.sidebar.button("Scrape and Process News"):
    with st.spinner("Scraping news and processing text..."):
        news_df = build_dataset(seed_urls)
        if not news_df.empty:
            # Combine headline + article
            news_df['full_text'] = news_df['news_headline'].astype(str) + '. ' + news_df['news_article']
            # Normalize text
            news_df['clean_text'] = normalize_corpus(news_df['full_text'])
            # Generate summaries
            news_df['summary'] = news_df['full_text'].apply(
                lambda text: generate_summary(text, stopword_list, reduction_ratio)
            )
            st.session_state['news_df'] = news_df
            st.success("News processed successfully!")
        else:
            st.error("No news data was collected. Please try again later.")

if "news_df" in st.session_state:
    news_df = st.session_state['news_df']
    st.subheader("News Data Overview")
    st.dataframe(news_df[['news_category', 'news_headline', 'summary']])
    
    if not news_df.empty:
        # Show details of a sample article
        st.subheader("Detailed View of a Sample Article")
        first_row = news_df.iloc[0]
        clean_text = first_row['clean_text']
        summary = first_row['summary']
        clean_text_word_count = len(clean_text.split())
        summary_word_count = len(summary.split())
        compression = 100 * (1 - summary_word_count / clean_text_word_count) if clean_text_word_count > 0 else 0

        st.write("**Category:**", first_row['news_category'])
        st.write("**Headline:**", first_row['news_headline'])

        with st.expander("View Cleaned Full Text"):
            st.write(clean_text)

        st.write("**Summary:**", summary)
        st.write("**Word Count (Cleaned Text):**", clean_text_word_count)
        st.write("**Word Count (Summary):**", summary_word_count)
        st.write("**Compression Achieved:**", f"{compression:.2f}%")
        
        # CSV Download
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')
        
        csv = convert_df(news_df)
        st.download_button(
            label="Download news_with_summary.csv",
            data=csv,
            file_name='news_with_summary.csv',
            mime='text/csv'
        )

# Add a custom footer
add_footer()
