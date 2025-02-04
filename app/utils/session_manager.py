class SessionManager:
    def __init__(self, stt, tts, query, audio_file):
        self.stt_provider = stt
        self.tts_provider = tts
        self.query_provider = query
        self.client_audio_file = audio_file

        self.transcribe_text = None
        self.query_text = None
        self.query_speech = None
        self.sentiment_profile = None

    # Getters
    def get_stt_provider(self):
        return self.stt_provider

    def get_tts_provider(self):
        return self.tts_provider

    def get_query_provider(self):
        return self.query_provider

    def get_client_audio_file(self):
        return self.client_audio_file

    def get_transcribe_text(self):
        return self.transcribe_text

    def get_query_text(self):
        return self.query_text

    def get_query_speech(self):
        return self.query_speech
    
    def get_sentiment_profile(self):
        return self.sentiment_profile
    
    def set_sentiment_profile(self, profile):
        self.sentiment_profile = profile

    # Setters
    def set_stt_provider(self, stt):
        self.stt_provider = stt

    def set_tts_provider(self, tts):
        self.tts_provider = tts

    def set_query_provider(self, query):
        self.query_provider = query

    def set_client_audio_file(self, audio_file):
        self.client_audio_file = audio_file

    def set_transcribe_text(self, text):
        self.transcribe_text = text

    def set_query_text(self, text):
        self.query_text = text

    def set_query_speech(self, speech):
        self.query_speech = speech


    
