from .word import Word
from .dictionary import Dictionary
from ..sderrors import DictionaryNotExistError, DictionaryAlreadyExistError, WordNotExistError
import re


class SmartDictionary(object):
    def __init__(self):
        self._dicts = dict()
        # Change name!
        self.addDictionary('Dict', 'Default dictionary')

    def words(self, name):
        if self.isDictExist(name):
            dict_words = list()
            # List all objects "Word" of this dictionary
            words = list(self._dicts.get(name).words().values())
            for i in range(len(words)):
                original = words[i].original()
                translate = words[i].translate()
                transcription = words[i].transcription()
                dict_words.append((original, translate, transcription))
            return dict_words
        else:
            # return False
            raise DictionaryNotExistError

    def dictionary(self, name):
        if self.isDictExist(name):
            dict_info = self._dicts.get(name)
            return (dict_info.name(), dict_info.description())
        else:
            # return False
            raise DictionaryNotExistError

    def dictionaries(self):
        dict_info = list()
        for name in self._dicts.keys():
            dict_info.append(self.dictionary(name))
        return dict_info

    # def isEmpty(self):
    #     return not bool(self._dicts)

    def quantity(self, name):
        if self.isDictExist(name):
            # List all objects "Word" of this dictionary
            words = list(self._dicts.get(name).words().values())
            return len(words)
        else:
            # return False
            raise DictionaryNotExistError

    def totalWords(self):
        # List all objects "Dictionary"
        dictionaries = list(self._dicts.values())
        quant = 0
        for i in range(len(dictionaries)):
            # List all objects "Word" of this dictionary
            words = list(dictionaries[i].words().values())
            quant = quant + len(words)
        return quant

    def addDictionary(self, name, description):
        name = self.trim(name)
        description = self.trim(description)
        if not self.isDictExist(name):
            self._dicts[name] = Dictionary(name, description)
            return True
        else:
            # return False
            raise DictionaryAlreadyExistError

    def deleteDictionary(self, name):
        if self.isDictExist(name):
            del self._dicts[name]
            return True
        else:
            # return False
            raise DictionaryNotExistError

    def changeDictionary(self, old_name, new_name, description):
        # Optimization!
        new_name = self.trim(new_name)
        description = self.trim(description)
        if self.isDictExist(old_name):
            if not self.isDictExist(new_name) or old_name == new_name:
                if old_name == new_name:
                    dictionary = self._dicts[old_name]
                    dictionary.setName(new_name)
                    dictionary.setDescription(description)
                else:
                    dictionary = self._dicts.pop(old_name)
                    dictionary.setName(new_name)
                    dictionary.setDescription(description)
                    self._dicts[new_name] = dictionary
                return True
            else:
                # return False
                raise DictionaryAlreadyExistError
        else:
            # return False
            raise DictionaryNotExistError

    def addWord(self, name, original, translate, transcrip, replace=False):
        original = self.trim(original)
        translate = self.trim(translate)
        transcrip = self.trim(transcrip)
        if self.isDictExist(name):
            if self.isWordExist(name, original):
                word = self._dicts[name].words()[original]
                if replace is False:
                    translate = word.translate() + ', ' + translate
                    if transcrip and word.transcription():
                        transcrip = word.transcription() + ', ' + transcrip
                word.setTranslate(translate)
                word.setTranscription(transcrip)
            else:
                new_word = Word(original, translate, transcrip)
                self._dicts[name].addWord(new_word)
            return True
        else:
            # return False
            raise DictionaryNotExistError

    def deleteWord(self, name, original):
        if self.isDictExist(name) and self.isWordExist(name, original):
            self._dicts[name].deleteWord(original)
            return True
        elif not self.isDictExist(name):
            raise DictionaryNotExistError
        else:
            raise WordNotExistError

    def changeWord(self, name, old_orig, orig, translate, transcription):
        orig = self.trim(orig)
        translate = self.trim(translate)
        transcription = self.trim(transcription)
        if self.isDictExist(name) and self.isWordExist(name, old_orig):
            new_word = Word(orig, translate, transcription)
            self._dicts[name].changeWord(old_orig, new_word)
            return True
        elif not self.isDictExist(name):
            raise DictionaryNotExistError
        else:
            raise WordNotExistError

    def isDictExist(self, name):
        return (name in (self._dicts.keys()))

    def isWordExist(self, name, original):
        if not self.isDictExist(name):
            raise DictionaryNotExistError
        return (original in self._dicts.get(name).words().keys())

    def trim(self, string):
        return re.sub('\s\s+', ' ', string.strip())
