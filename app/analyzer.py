"""
Módulo para análisis de sentimientos usando VADER de NLTK con lexicon extendido en español.
"""

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Extensión lexicon para palabras en español
sia.lexicon.update({
    "encantó": 2.0,
    "excelente": 2.5,
    "recomendable": 1.8,
    "horrible": -2.5,
    "malo": -2.0,
    "terrible": -3.0,
    "jamás": -1.5,
    "gustó": -1.0,
    "calidad": 1.5,
    "atención": 1.3,
    "muy": 0.5,
    "bueno": 1.5,
    "genial": 2.0,
})

def analyze_sentiment(text):
    """
    Analiza el sentimiento usando VADER (NLTK).

    Args:
        text (str): Texto a analizar.

    Returns:
        str: 'Positivo', 'Negativo' o 'Neutral'.
    """
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    print(f"Texto: {text} | Compound: {compound}")

    if compound >= 0.05:
        return 'Positivo'
    elif compound <= -0.05:
        return 'Negativo'
    else:
        return 'Neutral'
