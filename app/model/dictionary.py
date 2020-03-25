class Dictionary():
    def __init__(self, name, description=None):
        self._name = name
        self._description = description
        self._words = dict()

    def setName(self, name):
        self._name = name

    def setDescription(self, description):
        self._description = description

    def name(self):
        return self._name

    def description(self):
        return self._description

    def words(self):
        return self._words

    def word(self, word):
        return self._words.get(word)

    def addWord(self, word):
        self._words[word.original()] = word

    def deleteWord(self, word):
        del self._words[word]

    def changeWord(self, old, new):
        if old != new.original():
            del self._words[old]
        self.addWord(new)
