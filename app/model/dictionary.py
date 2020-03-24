from word import Word

class Dictionary():
	
	def __init__(self, _name, _description):
		self._name = _name
		self._description = _description
		self._words = dict()#or list()

	def setName(self, _name):
		self._name = _name

	def setDescription(self, _description):
		self._description = _description

	def name(self):
		return self._name

	def description(self):
		return self._description

	def words(self):
		return self._words

	def word(self, _word):
		return self._words.get(_word)

	def addWord(self, _word):
		self._words[_word.original()] = _word

	def deleteWord(self, _word):
		del self._words[_word]

	def changeWord(self, _old, _new):
		del self._words[_old]
		self._words[_new.original()] = _new
