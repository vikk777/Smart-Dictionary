from .word import Word
from .dictionary import Dictionary


class SmartDictionary(object):
    def __init__(self):
        self._dicts = dict()
        # Change name!
        self.addDictionary('Dict', 'Default dictionary')

    def words(self, name):
        dict_words = list()
        # List all objects "Word" of this dictionary
        words = list(self._dicts.get(name).words().values())
        for i in range(len(words)):
            original = words[i].original()
            translate = words[i].translate()
            transcription = words[i].transcription()
            # list(tuple()) or list(list())?
            dict_words.append((original, translate, transcription))
        return dict_words

    def dictionary(self, name):
        dict_info = self._dicts.get(name)
        return (dict_info.name(), dict_info.description())

    def dictionaries(self):
        dict_info = list()
        for name in list(self._dicts.keys()):
            dict_info.append(self.dictionary(name))
        return dict_info

    # def isEmpty(self):
    #     return not bool(self._dicts)

    def quantity(self, name):
        # List all objects "Word" of this dictionary
        words = list(self._dicts.get(name).words().values())
        return len(words)

    def totalWords(self):
        # List all objects "Dictionary"
        dictionaries = list(self._dicts.values())
        quant = 0
        for i in range(len(dictionaries)):
            # List all objects "Word" of this dictionary
            words = list(dictionaries[i].words().values())
            quant = quant + len(words)
        return quant

    def addDictionary(self, name, description=None):
        self._dicts[name] = Dictionary(name, description)
        return not self._dicts.get(name) is None

    def changeDictionary(self, old_name, new_name, description):
        dictionary = self._dicts.pop(old_name)
        dictionary.setName(new_name)
        dictionary.setDescription(description)
        self._dicts[new_name] = dictionary
        return not self._dicts.get(new_name) is None

    def deleteDictionary(self, name):
        del self._dicts[name]

    def addWord(self, name, original, translate, transcription=None):
        new_word = Word(original, translate, transcription)
        self._dicts[name].addWord(new_word)

    def deleteWord(self, name, original):
        self._dicts[name].deleteWord(original)

    def changeWord(self, name, old_orig, orig, translate, transcription=None):
        new_word = Word(orig, translate, transcription)
        self._dicts[name].changeWord(old_orig, new_word)
