import spacy
from textblob import TextBlob
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from heapq import nlargest

# Load NLP models
nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = SentimentIntensityAnalyzer()

def preprocess_text(text):
    """Preprocess the text by removing stopwords and punctuation."""
    doc = nlp(text)
    return " ".join([token.text for token in doc if not token.is_stop and not token.is_punct])

def summarize_text(text):
    """Summarize the text using a basic frequency-based approach."""
    # Tokenize the text and get word frequencies
    words = nltk.word_tokenize(text.lower())
    stopwords = nltk.corpus.stopwords.words('english')
    words = [word for word in words if word not in stopwords and word.isalpha()]
    
    word_freq = nltk.FreqDist(words)
    # Select top N frequent words
    most_common = nlargest(10, word_freq, key=word_freq.get)
    
    # Create a simple summary based on the frequent words
    summary = ' '.join(most_common)
    return summary

def analyze_sentiment(text):
    """Analyze sentiment using VaderSentiment."""
    sentiment = sentiment_analyzer.polarity_scores(text)
    return sentiment

def vectorize_text(text):
    """Convert the text to a vector using CountVectorizer."""
    vectorizer = CountVectorizer()
    text_vector = vectorizer.fit_transform([text]).toarray()
    return text_vector

def extract_entities(text):
    """Extract named entities from the text using spaCy."""
    doc = nlp(text)
    return [(entity.text, entity.label_) for entity in doc.ents]
