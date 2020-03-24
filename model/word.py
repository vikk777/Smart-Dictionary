
class Word():
	
	def __init__(self, _original, _translate, _transcription):
		self._original = _original 
		self._translate = _translate 
		self._transcription = _transcription

	def setOriginal(self, _original):
		self._original = _original 

	def setTranslate(self, _translate):
		self._translate = _translate 

	def setTranscription(self, _transcription):
		self._transcription = _transcription

	def original(self):
		return self._original

	def translate(self):
		return self._translate

	def transcription(self):
		return self._transcription