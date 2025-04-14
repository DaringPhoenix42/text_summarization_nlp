# # ===================== Step 1: Import Required Libraries =====================
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import os
# import re
# import unicodedata
# import nltk

# from contractions import CONTRACTION_MAP  # You need to provide CONTRACTION_MAP dictionary
# import spacy
# from nltk.tokenize.toktok import ToktokTokenizer

# tokenizer = ToktokTokenizer()
# tokens = tokenizer.tokenize("This is an example sentence.")
# print(tokens)

# # ===================== Step 2: Download Resources =====================
# nltk.download('stopwords')
# stopword_list = nltk.corpus.stopwords.words('english')
# stopword_list.remove('no')
# stopword_list.remove('not')

# tokenizer = ToktokTokenizer()
# nlp = spacy.load('en_core_web_sm')


# # -*- coding: utf-8 -*-
# """
# Created on Mon Aug 01 01:11:02 2016

# @author: DIP
# """

# CONTRACTION_MAP = { 
# "ain't": "am not",
# "aren't": "are not",
# "can't": "cannot",
# "can't've": "cannot have",
# "'cause": "because",
# "could've": "could have",
# "couldn't": "could not",
# "couldn't've": "could not have",
# "didn't": "did not",
# "doesn't": "does not",
# "doesn’t": "does not",
# "don't": "do not",
# "don’t": "do not",
# "hadn't": "had not",
# "hadn't've": "had not have",
# "hasn't": "has not",
# "haven't": "have not",
# "he'd": "he had",
# "he'd've": "he would have",
# "he'll": "he will",
# "he'll've": "he will have",
# "he's": "he is",
# "how'd": "how did",
# "how'd'y": "how do you",
# "how'll": "how will",
# "how's": "how is",
# "i'd": "i would",
# "i'd've": "i would have",
# "i'll": "i will",
# "i'll've": "i will have",
# "i'm": "i am",
# "i've": "i have",
# "isn't": "is not",
# "it'd": "it would",
# "it'd've": "it would have",
# "it'll": "it will",
# "it'll've": "it will have",
# "it's": "it is",
# "let's": "let us",
# "ma'am": "madam",
# "mayn't": "may not",
# "might've": "might have",
# "mightn't": "might not",
# "mightn't've": "might not have",
# "must've": "must have",
# "mustn't": "must not",
# "mustn't've": "must not have",
# "needn't": "need not",
# "needn't've": "need not have",
# "o'clock": "of the clock",
# "oughtn't": "ought not",
# "oughtn't've": "ought not have",
# "shan't": "shall not",
# "sha'n't": "shall not",
# "shan't've": "shall not have",
# "she'd": "she would",
# "she'd've": "she would have",
# "she'll": "she will",
# "she'll've": "she will have",
# "she's": "she is",
# "should've": "should have",
# "shouldn't": "should not",
# "shouldn't've": "should not have",
# "so've": "so have",
# "so's": "so is",
# "that'd": "that would",
# "that'd've": "that would have",
# "that's": "that is",
# "there'd": "there would",
# "there'd've": "there would have",
# "there's": "there is",
# "they'd": "they would",
# "they'd've": "they would have",
# "they'll": "they will",
# "they'll've": "they will have",
# "they're": "they are",
# "they've": "they have",
# "to've": "to have",
# "wasn't": "was not",
# "we'd": "we would",
# "we'd've": "we would have",
# "we'll": "we will",
# "we'll've": "we will have",
# "we're": "we are",
# "we've": "we have",
# "weren't": "were not",
# "what'll": "what will",
# "what'll've": "what will have",
# "what're": "what are",
# "what's": "what is",
# "what've": "what have",
# "when's": "when is",
# "when've": "when have",
# "where'd": "where did",
# "where's": "where is",
# "where've": "where have",
# "who'll": "who will",
# "who'll've": "who will have",
# "who's": "who is",
# "who've": "who have",
# "why's": "why is",
# "why've": "why have",
# "will've": "will have",
# "won't": "will not",
# "won't've": "will not have",
# "would've": "would have",
# "wouldn't": "would not",
# "wouldn't've": "would not have",
# "y'all": "you all",
# "y’all": "you all",
# "y'all'd": "you all would",
# "y'all'd've": "you all would have",
# "y'all're": "you all are",
# "y'all've": "you all have",
# "you'd": "you would",
# "you'd've": "you would have",
# "you'll": "you will",
# "you'll've": "you will have",
# "you're": "you are",
# "you've": "you have",
# "ain’t": "am not",
# "aren’t": "are not",
# "can’t": "cannot",
# "can’t’ve": "cannot have",
# "’cause": "because",
# "could’ve": "could have",
# "couldn’t": "could not",
# "couldn’t’ve": "could not have",
# "didn’t": "did not",
# "doesn’t": "does not",
# "don’t": "do not",
# "don’t": "do not",
# "hadn’t": "had not",
# "hadn’t’ve": "had not have",
# "hasn’t": "has not",
# "haven’t": "have not",
# "he’d": "he had",
# "he’d’ve": "he would have",
# "he’ll": "he will",
# "he’ll’ve": "he will have",
# "he’s": "he is",
# "how’d": "how did",
# "how’d’y": "how do you",
# "how’ll": "how will",
# "how’s": "how is",
# "i’d": "i would",
# "i’d’ve": "i would have",
# "i’ll": "i will",
# "i’ll’ve": "i will have",
# "i’m": "i am",
# "i’ve": "i have",
# "isn’t": "is not",
# "it’d": "it would",
# "it’d’ve": "it would have",
# "it’ll": "it will",
# "it’ll’ve": "it will have",
# "it’s": "it is",
# "let’s": "let us",
# "ma’am": "madam",
# "mayn’t": "may not",
# "might’ve": "might have",
# "mightn’t": "might not",
# "mightn’t’ve": "might not have",
# "must’ve": "must have",
# "mustn’t": "must not",
# "mustn’t’ve": "must not have",
# "needn’t": "need not",
# "needn’t’ve": "need not have",
# "o’clock": "of the clock",
# "oughtn’t": "ought not",
# "oughtn’t’ve": "ought not have",
# "shan’t": "shall not",
# "sha’n’t": "shall not",
# "shan’t’ve": "shall not have",
# "she’d": "she would",
# "she’d’ve": "she would have",
# "she’ll": "she will",
# "she’ll’ve": "she will have",
# "she’s": "she is",
# "should’ve": "should have",
# "shouldn’t": "should not",
# "shouldn’t’ve": "should not have",
# "so’ve": "so have",
# "so’s": "so is",
# "that’d": "that would",
# "that’d’ve": "that would have",
# "that’s": "that is",
# "there’d": "there would",
# "there’d’ve": "there would have",
# "there’s": "there is",
# "they’d": "they would",
# "they’d’ve": "they would have",
# "they’ll": "they will",
# "they’ll’ve": "they will have",
# "they’re": "they are",
# "they’ve": "they have",
# "to’ve": "to have",
# "wasn’t": "was not",
# "we’d": "we would",
# "we’d’ve": "we would have",
# "we’ll": "we will",
# "we’ll’ve": "we will have",
# "we’re": "we are",
# "we’ve": "we have",
# "weren’t": "were not",
# "what’ll": "what will",
# "what’ll’ve": "what will have",
# "what’re": "what are",
# "what’s": "what is",
# "what’ve": "what have",
# "when’s": "when is",
# "when’ve": "when have",
# "where’d": "where did",
# "where’s": "where is",
# "where’ve": "where have",
# "who’ll": "who will",
# "who’ll’ve": "who will have",
# "who’s": "who is",
# "who’ve": "who have",
# "why’s": "why is",
# "why’ve": "why have",
# "will’ve": "will have",
# "won’t": "will not",
# "won’t’ve": "will not have",
# "would’ve": "would have",
# "wouldn’t": "would not",
# "wouldn’t’ve": "would not have",
# "y’all": "you all",
# "y’all": "you all",
# "y’all’d": "you all would",
# "y’all’d’ve": "you all would have",
# "y’all’re": "you all are",
# "y’all’ve": "you all have",
# "you’d": "you would",
# "you’d’ve": "you would have",
# "you’ll": "you will",
# "you’ll’ve": "you will have",
# "you’re": "you are",
# "you’re": "you are",
# "you’ve": "you have",
# }

# # ===================== Step 3: Build Dataset from Inshorts =====================
# seed_urls = [
#     'https://inshorts.com/en/read/technology',
#     'https://inshorts.com/en/read/sports',
#     'https://inshorts.com/en/read/world'
# ]

# def build_dataset(seed_urls):
#     news_data = []
#     for url in seed_urls:
#         news_category = url.split('/')[-1]
#         data = requests.get(url)
#         soup = BeautifulSoup(data.content, 'html.parser')
#         news_articles = [{
#             'news_headline': headline.find('span', attrs={"itemprop": "headline"}).string,
#             'news_article': article.find('div', attrs={"itemprop": "articleBody"}).string,
#             'news_category': news_category
#         } for headline, article in zip(
#             soup.find_all('div', class_="news-card-title news-right-box"),
#             soup.find_all('div', class_="news-card-content news-right-box")
#         )]
#         news_data.extend(news_articles)
#     df = pd.DataFrame(news_data)
#     print(df.columns)
#     df = df[['headline', 'article', 'category']]

#     return df

# news_df = build_dataset(seed_urls)

# # ===================== Step 4: Text Preprocessing & Normalization =====================

# def strip_html_tags(text):
#     soup = BeautifulSoup(text, "html.parser")
#     return soup.get_text()

# def remove_accented_chars(text):
#     return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

# def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
#     contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
#                                       flags=re.IGNORECASE | re.DOTALL)
#     def expand_match(contraction):
#         match = contraction.group(0)
#         first_char = match[0]
#         expanded_contraction = contraction_mapping.get(match) \
#             if contraction_mapping.get(match) \
#             else contraction_mapping.get(match.lower())
#         return first_char + expanded_contraction[1:]
#     expanded_text = contractions_pattern.sub(expand_match, text)
#     return re.sub("'", "", expanded_text)

# def remove_special_characters(text, remove_digits=False):
#     pattern = r'[^a-zA-Z0-9\s]' if not remove_digits else r'[^a-zA-Z\s]'
#     return re.sub(pattern, '', text)

# def lemmatize_text(text):
#     doc = nlp(text)
#     return ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in doc])

# def remove_stopwords(text, is_lower_case=False):
#     tokens = tokenizer.tokenize(text)
#     tokens = [token.strip() for token in tokens]
#     if is_lower_case:
#         filtered_tokens = [token for token in tokens if token not in stopword_list]
#     else:
#         filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
#     return ' '.join(filtered_tokens)

# def normalize_corpus(corpus, html_stripping=True, contraction_expansion=True,
#                      accented_char_removal=True, text_lower_case=True,
#                      text_lemmatization=True, special_char_removal=True,
#                      stopword_removal=True, remove_digits=True):
#     normalized_corpus = []
#     for doc in corpus:
#         if html_stripping:
#             doc = strip_html_tags(doc)
#         if accented_char_removal:
#             doc = remove_accented_chars(doc)
#         if contraction_expansion:
#             doc = expand_contractions(doc)
#         if text_lower_case:
#             doc = doc.lower()
#         doc = re.sub(r'[\r|\n|\r\n]+', ' ', doc)
#         if text_lemmatization:
#             doc = lemmatize_text(doc)
#         if special_char_removal:
#             special_char_pattern = re.compile(r'([{.(-)!}])')
#             doc = special_char_pattern.sub(" \\1 ", doc)
#             doc = remove_special_characters(doc, remove_digits=remove_digits)
#         doc = re.sub(' +', ' ', doc)
#         if stopword_removal:
#             doc = remove_stopwords(doc, is_lower_case=text_lower_case)
#         normalized_corpus.append(doc)
#     return normalized_corpus

# # Add full text column and normalize
# news_df['full_text'] = news_df['news_headline'].astype(str) + '. ' + news_df['news_article']
# news_df['clean_text'] = normalize_corpus(news_df['full_text'])

# # ===================== Step 5: Frequency-Based Extractive Summarization =====================

# # Sentence Tokenization
# def split_sentences(text):
#     return re.split(r'(?<=[.!?]) +', text)

# # Word Tokenization
# def split_words(text):
#     return re.findall(r'\w+', text.lower())

# # Frequency Table
# def build_frequency_table(text, stopwords):
#     words = split_words(text)
#     freq_table = {}
#     for word in words:
#         if word in stopwords:
#             continue
#         freq_table[word] = freq_table.get(word, 0) + 1
#     return freq_table

# # Sentence Scoring
# def score_sentences(sentences, freq_table):
#     sentence_scores = {}
#     for sentence in sentences:
#         sentence_words = split_words(sentence)
#         if len(sentence_words) == 0:
#             continue
#         score = sum(freq_table.get(word, 0) for word in sentence_words)
#         sentence_scores[sentence] = score / len(sentence_words)
#     return sentence_scores

# # Generate Summary
# def generate_summary(text, stopwords, reduction_ratio=0.3):
#     sentences = split_sentences(text)
#     freq_table = build_frequency_table(text, stopwords)
#     sentence_scores = score_sentences(sentences, freq_table)
#     top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max(1, int(len(sentences) * reduction_ratio))]
#     summary = ' '.join([sentence for sentence in sentences if sentence in top_sentences])
#     return summary

# # Apply summarizer to DataFrame
# news_df['summary'] = news_df['clean_text'].apply(lambda text: generate_summary(text, stopword_list, reduction_ratio=0.3))

# # ===================== Step 6: Output =====================
# # Print sample summaries
# print(news_df[['news_headline', 'clean_text', 'summary']].head())

# # Save to CSV
# news_df.to_csv('news_with_summary.csv', index=False, encoding='utf-8')











































































import requests
from bs4 import BeautifulSoup
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import spacy
import string
import time

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Load Spacy model for NLP tasks
nlp = spacy.load('en_core_web_sm')

# Headers to bypass basic scraping restrictions
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def fetch_news(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Improved selectors with fallbacks
            headline = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'No headline found'
            
            # More robust article text extraction
            article_body = soup.find_all(['p', 'article-body', 'div.article__body'])
            article = " ".join([p.get_text(strip=True) for p in article_body]) if article_body else 'No article text found'
            
            # Category extraction with multiple fallbacks
            category = (soup.find('meta', {'property': 'article:section'}) or 
                       soup.find('a', {'class': 'category'}) or 
                       soup.find('meta', {'name': 'category'}))
            category = category.get_text(strip=True) if category and hasattr(category, 'get_text') else (
                category['content'] if category and 'content' in category.attrs else 'No category found'
            )
            
            return headline, article, category
        else:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return None, None, None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None, None

def build_dataset(seed_urls):
    headlines, articles, categories = [], [], []
    for url in seed_urls:
        print(f"Fetching data from {url}")
        headline, article, category = fetch_news(url)
        if headline and article and category:
            headlines.append(headline)
            articles.append(article)
            categories.append(category)
        else:
            print(f"No valid data found for {url}.")
        
        time.sleep(1)  # Adding delay to avoid overloading the server
    
    if headlines:
        df = pd.DataFrame({
            'news_headline': headlines,
            'news_article': articles,
            'news_category': categories
        })
        print(f"\nData collected:\n{df.head()}")
        return df
    else:
        print("No data collected! Exiting function.")
        return pd.DataFrame()

def clean_text(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens 
              if word not in string.punctuation 
              and word.lower() not in stopwords.words('english')]
    return " ".join(tokens)

def summarize_text(texts):
    # Filter out invalid articles
    valid_texts = [text for text in texts if text != 'No article text found']
    
    if not valid_texts:
        print("\nNo valid articles to summarize.")
        return
    
    # Clean and summarize each article individually
    print("\nArticle Summaries:")
    for i, text in enumerate(valid_texts):
        cleaned = clean_text(text)
        
        # Simple summarization by taking first 3 sentences
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        summary = " ".join(sentences[:3]) if len(sentences) > 3 else text
        
        print(f"\nSummary for Article {i+1}:")
        print(f"{summary}\n")
        print("-" * 50)
    
    # Additional analysis of similarities
    cleaned_texts = [clean_text(text) for text in valid_texts]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(cleaned_texts)
    similarities = cosine_similarity(tfidf_matrix)
    
    print("\nCosine Similarity Matrix:")
    print(similarities)

if __name__ == "__main__":
    seed_urls = [
        "https://www.bbc.com/news/articles/c93gy91y43vo",
        "https://edition.cnn.com/2025/04/12/politics/rfk-jrs-long-complicated-history-with-the-measles-vaccines/index.html",
        "https://www.reuters.com/markets/commodities/indias-polished-diamond-exports-hit-two-decade-low-industry-group-says-2025-04-14/"
    ]
    
    news_df = build_dataset(seed_urls)
    
    if not news_df.empty:
        summarize_text(news_df['news_article'].tolist())
    else:
        print("No data available for summarization.")

