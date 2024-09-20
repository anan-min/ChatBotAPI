class RequestData:
    def __init__(self, stt_provider, tts_provider, query_provider, audio_file):
        self.stt_provider = stt_provider
        self.tts_provider = tts_provider
        self.query_provider = query_provider
        self.audio_file = audio_file

    def get_stt_provider(self):
        return self.stt_provider
    
    def get_tts_provider(self):
        return self.tts_provider
    
    def get_query_provider(self):
        return self.query_provider
    
    def get_audio_file(self):
        return self.audio_file
    