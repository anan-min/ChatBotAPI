from app.utils.session_manager import SessionManager
from textblob import TextBlob
from aiogoogletrans import Translator

# Define thresholds for sentiment profiles
THRESHOLDS = {
    "HAPPY": 0.5,
    "SAD": 0,
    "ANGRY": -0.5,
}

class SentimentProcessor:
    def __init__(self):
        self.translator = Translator()  # Initialize translator

    async def process(self, session: SessionManager):
        # Retrieve text from the session
        text = session.get_query_text()

        # Translate the text (synchronous method)
        translation = await self.translator.translate(text, src='th', dest='en')
        translated_text = translation.text
        print(f"Translated Text: {translated_text}")

        # Perform sentiment analysis
        blob = TextBlob(translated_text)
        polarity = blob.sentiment.polarity
        print(f"Original Text: {text}")
        print(f"Polarity: {polarity}")

        # Determine sentiment profile based on polarity
        if polarity > THRESHOLDS["HAPPY"]:
            session.set_sentiment_profile("HAPPY")
        elif THRESHOLDS["SAD"] <= polarity <= THRESHOLDS["HAPPY"]:
            session.set_sentiment_profile("NEUTRAL")
        elif THRESHOLDS["ANGRY"] <= polarity < THRESHOLDS["SAD"]:
            session.set_sentiment_profile("SAD")
        else:
            session.set_sentiment_profile("ANGRY")
