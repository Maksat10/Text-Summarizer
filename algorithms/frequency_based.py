import nltk
import string

nltk.download('punkt')
nltk.download('stopwords')

stopwords = nltk.corpus.stopwords.words('english')

def preprocess(text):
    formatted_text = text.lower()
    tokens = nltk.word_tokenize(formatted_text)
    tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
    return tokens

def calculate_word_frequencies(tokens):
    frequency = nltk.FreqDist(tokens)
    return frequency

def score_sentences(sentences, word_frequencies):
    sentence_scores = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]
    return sentence_scores

def summarize(text, min_sentences=5, fraction_of_total=0.1):
    sentences = nltk.sent_tokenize(text)
    tokens = preprocess(text)
    word_frequencies = calculate_word_frequencies(tokens)
    sentence_scores = score_sentences(sentences, word_frequencies)
    
    number_of_sentences = max(min_sentences, int(len(sentences) * fraction_of_total))
    
    best_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:number_of_sentences]
    return ' '.join(best_sentences)
