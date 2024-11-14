import nltk
import heapq
from collections import Counter

nltk.download('punkt')

def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    return tokens

def calculate_sentences_score(sentences, important_words, distance):
    scores = []
    for sentence_index, sentence in enumerate(sentences):
        word_index = [i for i, word in enumerate(sentence) if word in important_words]
        if not word_index:
            continue
        groups = []
        group = [word_index[0]]
        for i in range(1, len(word_index)):
            if word_index[i] - word_index[i - 1] < distance:
                group.append(word_index[i])
            else:
                groups.append(group)
                group = [word_index[i]]
        groups.append(group)
        max_group_score = max((len(group) ** 2 / (group[-1] - group[0] + 1)) for group in groups)
        scores.append((max_group_score, sentence_index))
    return scores

def summarize(text, top_n_words=100, distance=2, min_sentences=5, fraction_of_total=0.1):
    original_sentences = nltk.sent_tokenize(text)
    formatted_sentences = [preprocess(sentence) for sentence in original_sentences]
    words = [word for sentence in formatted_sentences for word in sentence]
    frequency = Counter(words)
    top_n_words = [word for word, _ in frequency.most_common(top_n_words)]
    sentences_score = calculate_sentences_score(formatted_sentences, top_n_words, distance)
    

    number_of_sentences = max(min_sentences, int(len(original_sentences) * fraction_of_total))
    
    best_sentences = heapq.nlargest(number_of_sentences, sentences_score)
    best_sentences = [original_sentences[index] for _, index in best_sentences]
    return ' '.join(best_sentences)

