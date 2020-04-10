from .word import Word
from .dictionary import Dictionary
from .test_manager import TestManager
from ..sderrors import DictionaryNotExistError, DictionaryAlreadyExistError, WordNotExistError
import re
import app.consts as consts
from datetime import date


class SmartDictionary(object):
    def __init__(self):
        self._dicts = dict()
        self._testManager = TestManager()

        # Change name!
        self.addDictionary('Dict', 'Default dictionary')

    def words(self, name):
        if self.isDictExist(name):
            dict_words = list()
            # List all objects "Word" of this dictionary
            words = list(self._dicts.get(name).words().values())
            for word in words:
                dict_words.append({'original': word.original(),
                                   'translate': word.translate(),
                                   'transcription': word.transcription(),
                                   'updateTime': word.updateTime()})
            return dict_words

        else:
            raise DictionaryNotExistError

    def allWords(self):
        all_words = list()

        for name in self._dicts:
            all_words.extend(self.words(name))

        return all_words

    def dictionary(self, name):
        if self.isDictExist(name):
            dict_info = self._dicts.get(name)
            return (dict_info.name(), dict_info.description())
        else:
            raise DictionaryNotExistError

    def dictionaries(self):
        dict_info = list()

        for name in self._dicts:
            dict_info.append(self.dictionary(name))

        return dict_info

    def quantity(self, name):
        if self.isDictExist(name):
            # List all objects "Word" of this dictionary
            words = list(self._dicts.get(name).words().values())
            return len(words)

        else:
            raise DictionaryNotExistError

    def totalWords(self):
        # List all objects "Dictionary"
        dictionaries = list(self._dicts.values())
        quant = 0

        for dictionary in dictionaries:
            # List all objects "Word" of this dictionary
            words = list(dictionary.words().values())
            quant = quant + len(words)

        return quant

    def addDictionary(self, name, description):
        name = self.trim(name)
        description = self.trim(description)

        if not self.isDictExist(name):
            self._dicts[name] = Dictionary(name, description)
            return True

        else:
            raise DictionaryAlreadyExistError

    def deleteDictionary(self, name):
        if self.isDictExist(name):
            del self._dicts[name]
            return True

        else:
            raise DictionaryNotExistError

    def changeDictionary(self, old_name, new_name, description):
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
                raise DictionaryAlreadyExistError

        else:
            raise DictionaryNotExistError

    def addWord(self, name, original, translate, transcrip, time, replace=False):
        original = self.trim(original)
        translate = self.trim(translate)
        transcrip = self.trim(transcrip)

        if self.isDictExist(name):

            if self.isWordExist(name, original):
                word = self._dicts[name].words()[original]

                if not replace:
                    translate = word.translate() + ', ' + translate

                    if transcrip and word.transcription():
                        transcrip = word.transcription() + ', ' + transcrip

                word.setTranslate(translate)
                word.setUpdateTime(time)
                if transcrip:
                    word.setTranscription(transcrip)

            else:
                new_word = Word(original, translate, transcrip, time)
                self._dicts[name].addWord(new_word)

            return True

        else:
            raise DictionaryNotExistError

    def deleteWord(self, name, original):
        if self.isDictExist(name) and self.isWordExist(name, original):
            self._dicts[name].deleteWord(original)
            return True

        elif not self.isDictExist(name):
            raise DictionaryNotExistError

        else:
            raise WordNotExistError

    def changeWord(self, name, old_orig, orig, translate, transcription, time):
        orig = self.trim(orig)
        translate = self.trim(translate)
        transcription = self.trim(transcription)

        if self.isDictExist(name) and self.isWordExist(name, old_orig):
            new_word = Word(orig, translate, transcription, time)
            self._dicts[name].changeWord(old_orig, new_word)
            return True

        elif not self.isDictExist(name):
            raise DictionaryNotExistError

        else:
            raise WordNotExistError

    def isDictExist(self, name):
        return name in self._dicts

    def isWordExist(self, name, original):
        if not self.isDictExist(name):
            raise DictionaryNotExistError

        return original in self._dicts.get(name).words()

    def trim(self, string):
        string = re.sub('\s\s+', ' ', string.strip())
        return re.sub('\s*,', ', ', string)

    def testInit(self, name, period='-1'):
        if name == consts.MISTAKE_DICT:
            initDict = dict()
            for questions, answer in self._testManager.mistakesAnswers().items():
                initDict.update({questions: answer})

        else:
            if name == consts.ALL_DICTS:
                words = self.allWords()
            elif self.isDictExist(name):
                words = self.words(name)
            else:
                raise DictionaryNotExistError

            period = int(period)
            if period >= 0:
                lastTime = words[-1].get('updateTime')
                lastTime = date.fromtimestamp(lastTime)
                # lastTime = date(lastTime.year, lastTime.month, lastTime.day - period)
                new_words = list()

                for word in words:
                    if (lastTime - date.fromtimestamp(word['updateTime'])).days <= period:
                        new_words.append(word)
                words = new_words

            initDict = dict()

            for word in words:
                initDict.update({word.get('original'): word.get('translate')})

            for word in words:
                initDict.update({word.get('translate').split(', ')[0]: word.get('original')})

        self._testManager.setQuestions(initDict)
        self._testManager.setTempQuestions(list(initDict.keys()))

        return True

    def testIsInit(self):
        return True if self._testManager._questions else False

    def nextQuestion(self):
        questions = self._testManager.tempQuestions()

        if questions:
            question = questions.pop(0)
            self._testManager.setTempQuestions(questions)
            return question

        else:
            return ''

    def addAnswer(self, answer):
        # answer - tuple()
        # answ = list()
        # answ = (self.trim(answer[0]), self.trim(answer[1]))
        self._testManager.setAnswers((self.trim(answer[0]),
                                      self.trim(answer[1])))

    def testResult(self):
        return self._testManager.check()

    def haveMistakes(self):
        return True if self._testManager.mistakesAnswers() else False

    # 1-ый способ
    # def importWords(self, dictionary, words, updateTime):
    #     if self.isDictExist(dictionary):
    #         words = words.split('\n')
    #         for word in words:
    #             self.addWord(dictionary,
    #                          self.trim(word).split(' - ')[0],
    #                          self.trim(word).split(' - ')[1],
    #                          None,
    #                          updateTime)
    #         return True
    #     else:
    #         raise DictionaryNotExistError

    # 2-ый способ
    def importWords(self, dictionary, words, updateTime):
        if self.isDictExist(dictionary):
            words = words.split('\n')
            # Change regular
            # regex = re.compile('(\w+)\s*-\s*(\w+(,?\s*\w*)*)')
            regex = re.compile('(\w+)\s*-\s*(.*)')
            for word in words:
                word = regex.findall(self.trim(word))
                self.addWord(dictionary,
                             word[0][0],
                             word[0][1],
                             None,
                             updateTime)
            return True
        else:
            raise DictionaryNotExistError
