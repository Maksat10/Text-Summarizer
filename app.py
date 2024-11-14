from flask import Flask, render_template, request
import requests
from algorithms import frequency_based, luhn, cosine_similarity
import spacy
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        text = request.form['input_text']
        model_choice = request.form['model_choice']
        number_of_sentences = int(request.form.get('number_of_sentences', 5))
        final_reading_time = readingTime(text)

        min_sentences = 5
        fraction_of_total = 0.1
        if model_choice == 'default':
            summary = frequency_based.summarize(text, min_sentences=min_sentences, fraction_of_total=fraction_of_total)
        elif model_choice == 'Frequency_based':
            summary = frequency_based.summarize(text, min_sentences=min_sentences, fraction_of_total=fraction_of_total)
        elif model_choice == 'luhn':
            summary = luhn.summarize(text, top_n_words=100, distance=2, min_sentences=min_sentences, fraction_of_total=fraction_of_total)
        elif model_choice == 'Cosine_similarity':
            summary = cosine_similarity.summarize(text, number_of_sentences=number_of_sentences)
        summary_reading_time = readingTime(summary)

        return render_template('summary.html', ctext=text, final_summary=summary, 
                               final_reading_time=final_reading_time, 
                               summary_reading_time=summary_reading_time)
    except Exception as e:
        return str(e), 400


def get_text(url):
    response = requests.get(url, headers={'User-Agent': "Magic Browser"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        fetched_text = ' '.join(p.text for p in soup.find_all('p'))
        return fetched_text
    else:
        return "Error fetching page"


@app.route('/process_url',methods=['GET','POST'])
def process_url():
	start = time.time()
	if request.method == 'POST':
		input_url = request.form['input_url']
		raw_text = get_text(input_url)
		final_reading_time = readingTime(raw_text)
		final_summary = cosine_similarity.summarize(raw_text)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('summary.html',ctext=raw_text,
                        final_summary=final_summary,
                        final_time=final_time,
                        final_reading_time=final_reading_time,
                        summary_reading_time=summary_reading_time)

if __name__ == '__main__':
    app.run(debug=True)
