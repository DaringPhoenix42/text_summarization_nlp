# ===================== Step 1: Import Required Libraries =====================
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
import unicodedata
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
from contractions import CONTRACTION_MAP  # You need to provide CONTRACTION_MAP dictionary
import spacy

# ===================== Step 2: Download Resources =====================
nltk.download('stopwords')
nltk.download('punkt')
stopword_list = nltk.corpus.stopwords.words('english')
stopword_list.remove('no')
stopword_list.remove('not')

tokenizer = ToktokTokenizer()
nlp = spacy.load('en_core_web_sm')

# ===================== Step 3: Build Dataset from Inshorts =====================
seed_urls = [
    'https://inshorts.com/en/read/technology',
    'https://inshorts.com/en/read/sports',
    'https://inshorts.com/en/read/world'
]

def build_dataset(seed_urls):
    news_data = []

    for url in seed_urls:
        print(f"Scraping from: {url}")
        news_category = url.split('/')[-1]
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'html.parser')

        # Use itemprop to get relevant elements directly
        headlines = soup.find_all('span', itemprop='headline')
        articles = soup.find_all('div', itemprop='articleBody')

        print(f"Found {len(headlines)} headlines and {len(articles)} articles in category '{news_category}'")

        for headline, article in zip(headlines, articles):
            news_data.append({
                'news_headline': headline.get_text(strip=True),
                'news_article': article.get_text(strip=True),
                'news_category': news_category
            })

    if not news_data:
        print("No articles were scraped. Structure might have changed.")
    else:
        print(f"Total articles collected: {len(news_data)}")

    return pd.DataFrame(news_data)

news_df = build_dataset(seed_urls)

# ===================== Step 4: Text Preprocessing & Normalization =====================

def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_accented_chars(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        return first_char + expanded_contraction[1:]
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

def normalize_corpus(corpus, html_stripping=True, contraction_expansion=True,
                     accented_char_removal=True, text_lower_case=True,
                     text_lemmatization=True, special_char_removal=True,
                     stopword_removal=True, remove_digits=True):
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
        doc = re.sub(r'[\r|\n|\r\n]+', ' ', doc)
        if text_lemmatization:
            doc = lemmatize_text(doc)
        if special_char_removal:
            special_char_pattern = re.compile(r'([{.(-)!}])')
            doc = special_char_pattern.sub(" \\1 ", doc)
            doc = remove_special_characters(doc, remove_digits=remove_digits)
        doc = re.sub(' +', ' ', doc)
        if stopword_removal:
            doc = remove_stopwords(doc, is_lower_case=text_lower_case)
        normalized_corpus.append(doc)
    return normalized_corpus

# Add full text column and normalize
news_df['full_text'] = news_df['news_headline'].astype(str) + '. ' + news_df['news_article']
news_df['clean_text'] = normalize_corpus(news_df['full_text'])

# ===================== Step 5: Frequency-Based Extractive Summarization =====================

# Sentence Tokenization
def split_sentences(text):
    return sent_tokenize(text)

# Word Tokenization
def split_words(text):
    return word_tokenize(text.lower())

# Frequency Table
def build_frequency_table(text, stopwords):
    words = split_words(text)
    freq_table = {}
    for word in words:
        if word in stopwords:
            continue
        freq_table[word] = freq_table.get(word, 0) + 1
    return freq_table

# Sentence Scoring
def score_sentences(sentences, freq_table):
    sentence_scores = {}
    for sentence in sentences:
        sentence_words = split_words(sentence)
        if len(sentence_words) == 0:
            continue
        score = sum(freq_table.get(word, 0) for word in sentence_words)
        sentence_scores[sentence] = score / len(sentence_words)
    return sentence_scores

# Generate Summary
def generate_summary(text, stopwords, reduction_ratio=0.3):
    sentences = split_sentences(text)
    freq_table = build_frequency_table(text, stopwords)
    sentence_scores = score_sentences(sentences, freq_table)
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max(1, int(len(sentences) * reduction_ratio))]
    summary = ' '.join([sentence for sentence in sentences if sentence in top_sentences])
    return summary

# Apply summarizer to DataFrame
news_df['summary'] = news_df['full_text'].apply(lambda text: generate_summary(text, stopword_list, reduction_ratio=0.3))

# ===================== Step 6: Output =====================
# Print sample summaries
# Check if dataframe is not empty before accessing
if not news_df.empty:
    first_row = news_df.iloc[0]
    
    clean_text = first_row['clean_text']
    summary = first_row['summary']
    
    clean_text_word_count = len(clean_text.split())
    summary_word_count = len(summary.split())
    
    print("🧾 Cleaned Full Text:\n", clean_text, f"\n\n🔢 Word Count: {clean_text_word_count}\n")
    print("📝 Summary:\n", summary, f"\n\n🔢 Word Count: {summary_word_count}\n")
    
    compression = 100 * (1 - summary_word_count / clean_text_word_count) if clean_text_word_count > 0 else 0
    print(f"📉 Compression Achieved: {compression:.2f}%")
else:
    print("❌ No data available to compare clean text and summary.")

# Save to CSV
news_df.to_csv('news_with_summary.csv', index=False, encoding='utf-8')