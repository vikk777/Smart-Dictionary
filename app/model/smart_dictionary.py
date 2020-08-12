from .dictionary import Dictionary
from .test_manager import TestManager
from .user import User
from ..sderrors import DictionaryNotExistError,\
    DictionaryAlreadyExistError,\
    InvalidUsernameOrPasswordError,\
    UserAlreadyExistError,\
    QuestionAlreadyAddedError
import app.functions as functions
import app.consts as consts
from datetime import date
from flask_login import logout_user, current_user

# !!! trim username


class SmartDictionary():
    def __init__(self):
        self._user = User()
        self._dict = Dictionary()
        self._testManager = TestManager()

# Dictionary --------------------------------------------------

    def addDictionary(self, name, description):
        name = functions.trim(name)
        description = functions.trim(description)

        if not self._dict.isExist(current_user, name):
            self._dict.add(current_user, name, description)
            return True

        else:
            raise DictionaryAlreadyExistError

    def dictionaries(self):
        """Get all dict's name and description in list(tuple())"""
        temp = self._dict.all(current_user)
        dicts = list()

        for dict_ in temp:
            dicts.append((dict_.name,
                          dict_.description,
                          self.quantity(dict_.name)))

        return dicts

    def dictionary(self, name):
        dict_ = self._dict.get(current_user, name)
        if dict_:
            return (dict_.name,
                    dict_.description,
                    self.quantity(dict_.name))
        else:
            raise DictionaryNotExistError

    def changeDictionary(self, oldName, newName, description):
        newName = functions.trim(newName)
        description = functions.trim(description)

        if self._dict.isExist(current_user, oldName):
            if self._dict.isExist(current_user, newName)\
                    and oldName != newName:
                raise DictionaryAlreadyExistError
            else:
                self._dict.change(current_user, oldName, newName, description)
                return True

        else:
            raise DictionaryNotExistError

    def deleteDictionary(self, name):
        if self._dict.isExist(current_user, name):
            self._dict.delete(current_user, name)
        else:
            raise DictionaryNotExistError

# Words --------------------------------------------------

    def addWord(self, dictName, original, translate,
                transcription, time, replace=False):
        original = functions.trim(original)
        translate = functions.trim(translate)
        transcription = functions.trim(transcription)

        if self._dict.isExist(current_user, dictName):
            self._dict.addWord(current_user, dictName, original, translate,
                               transcription, time, replace)
            return True
        else:
            raise DictionaryNotExistError

    def words(self, name):
        if self._dict.isExist(current_user, name):
            return self._dict.words(current_user, name)
        else:
            raise DictionaryNotExistError

    def deleteWord(self, name, original):
        if self._dict.isExist(current_user, name):
            self._dict.deleteWord(current_user, name, original)
            return True
        else:
            raise DictionaryNotExistError

    def changeWord(self, name, old, new, translate, transcription, time):
        new = functions.trim(new)
        translate = functions.trim(translate)
        transcription = functions.trim(transcription)

        if self._dict.isExist(current_user, name):
            self._dict.changeWord(current_user, name, old, new,
                                  translate, transcription, time)
            return True
        else:
            raise DictionaryNotExistError

    def quantity(self, name):
        """Quantity of words in dictionary"""
        return len(self.words(name))

    def totalWords(self):
        total = 0
        for dict_ in self.dictionaries():
            total += self.quantity(dict_[0])
        return total

    def importWords(self, name, words, time):
        if self._dict.isExist(current_user, name):
            words = words.split('\r\n')
            addedWords = list()

            for word in words:
                word = functions.search(consts.regexp.IMPORT, word)
                if word:
                    self.addWord(name, word[1], word[2], '', time)

                    if word[1] not in addedWords:
                        addedWords.append((word[1], word[2]))
            return addedWords
        else:
            raise DictionaryNotExistError

# Test --------------------------------------------------

    def testInit(self, name, period=consts.period.ALL_I):
        # self._testManager.init(current_user.id)
        initDict = dict()

        if name == consts.ADDED_WORDS:
            initDict.update(self._testManager.questions(current_user.id))

        # dictionary of mistakes
        elif name == consts.MISTAKE_DICT:
            # for question, answer in\
            # self._testManager.mistakes(current_user.id).items():
            # initDict.update({question: answer})
            # initDict.update({answer: question})
            initDict.update(self._testManager.mistakes(current_user.id))

        else:
            if name == consts.ALL_DICTS:
                words = self._dict.allWords(current_user)
            else:
                words = self.words(name)

            # filter words by period
            period = int(period)
            if period >= 0:
                lastTime = words[-1].get('updateTime')
                lastTime = date.fromtimestamp(lastTime)
                new_words = list()

                for word in words:
                    if (lastTime - date.fromtimestamp(word['updateTime'])).\
                            days <= period:
                        new_words.append(word)
                words = new_words

            for word in words:
                initDict.update({word.get('original'): word.get('translate')})

        reverse = dict()
        for question, answer in initDict.items():
            reverse.update({answer: question})
        initDict.update(reverse)

        self._testManager.setQuestions(current_user.id, initDict)
        # self._testManager.setTempQuestions(current_user.id,
        #                                    list(initDict.keys()))

        return True

    def isTestInit(self):
        return self._testManager.isInit(current_user.id)

    def addQuestion(self, question, answer):
        # if not self.isTestInit():
        #     self._testManager.init(current_user.id)

        if not self._testManager.haveQuestion(current_user.id, question):
            self._testManager.addQuestion(current_user.id, question, answer)
            return True
        else:
            raise QuestionAlreadyAddedError

    def nextQuestion(self):
        question = self._testManager.nextQuestion(current_user.id)

        if question:
            # position = randint(0, self._testManager.totalTemp(
            #     current_user.id) - 1)
            # question = questions.pop(position)
            # question = questions.pop(0)
            # questions is refer to _tempQuestions
            # self._testManager.setTempQuestions(current_user.id, questions)
            return {'question': question,
                    'progress': self._testManager.progress(current_user.id)}

        else:
            return {}

    def addAnswer(self, question, answer):
        # answer - tuple()
        self._testManager.setAnswer(current_user.id,
                                    functions.trim(question.lower()),
                                    functions.trim(answer.lower()))

    def testResult(self):
        return self._testManager.check(current_user.id)

    def mistakes(self):
        return self._testManager.mistakes(current_user.id)

    def addedWords(self):
        return self._testManager.questions(current_user.id)

    def abortTest(self):
        return self._testManager.abortTest(current_user.id)

# Users --------------------------------------------------

    def registerUser(self, name, password):
        name = functions.trim(name)

        if self._user.register(name, password):
            self.loginUser(name, password, True)
            self.addDictionary('Dict', 'Default dictionary')
        else:
            raise UserAlreadyExistError

    def loginUser(self, name, password, remember):
        name = functions.trim(name)

        if not self._user.login(name, password, remember):
            raise InvalidUsernameOrPasswordError

    def logoutUser(self):
        logout_user()

    def search(self, find):
        found = self._dict.search(current_user, find)
        words = dict()

        for word in found:
            if not words.get(word.dictionary.name):
                words[word.dictionary.name] = list()

            words[word.dictionary.name].append({
                'original': word.original,
                'translate': word.translate
            })
        return words
