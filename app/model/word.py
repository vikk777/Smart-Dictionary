class Word():
    def __init__(self, original, translate, transcription=None):
        self._original = original
        self._translate = translate
        self._transcription = transcription

    def setOriginal(self, original):
        self._original = original

    def setTranslate(self, translate):
        self._translate = translate

    def setTranscription(self, transcription):
        self._transcription = transcription

    def original(self):
        return self._original

    def translate(self):
        return self._translate

    def transcription(self):
        return self._transcription
