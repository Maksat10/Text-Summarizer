import re
import nltk
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

nltk.download('punkt')
nltk.download('stopwords')

stopwords = nltk.corpus.stopwords.words('english')

def preprocess(text):
    formatted_text = text.lower()
    tokens = nltk.word_tokenize(formatted_text)
    tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
    return ' '.join(tokens)

def build_similarity_matrix(sentences):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

def rank_sentences(similarity_matrix, sentences, top_n):
    sentence_similarity_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    return [ranked_sentences[i][1] for i in range(top_n)]

def summarize_chunk(text, number_of_sentences=5):
    sentences = nltk.sent_tokenize(text)
    formatted_sentences = [preprocess(sentence) for sentence in sentences]
    similarity_matrix = build_similarity_matrix(formatted_sentences)
    summary_sentences = rank_sentences(similarity_matrix, sentences, number_of_sentences)
    return ' '.join(summary_sentences)

def chunk_text(text, max_words=1000):
    words = text.split()
    chunks = [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    return chunks

def summarize(text, number_of_sentences=5):
    chunks = chunk_text(text)
    chunk_summaries = [summarize_chunk(chunk, number_of_sentences) for chunk in chunks]
    return ' '.join(chunk_summaries)

