from app import db
from .word import Word
from .dictionary_model import DictionaryModel
from ..sderrors import WordNotExistError


class Dictionary():
    """Class-decorator upon database.DictionaryModel"""

    def __init__(self):
        self._word = Word()

    def add(self, user, name, description):
        """Add dictionary for user"""
        dictionary = DictionaryModel(name=name,
                                     description=description,
                                     user=user)
        db.session.add(dictionary)
        db.session.commit()
        return True

    def all(self, user):
        """Get all dictionaries"""
        return DictionaryModel.query.filter_by(user=user).all()

    def get(self, user, name):
        """Get user's dict"""
        return DictionaryModel.query.filter_by(user=user,
                                               name=name).first()

    def delete(self, user, name):
        """Delete user's dict"""
        dictionary = self.get(user, name)
        db.session.delete(dictionary)
        db.session.commit()
        return True

    def change(self, user, oldName, newName, description):
        dictionary = self.get(user, oldName)
        if oldName != newName or dictionary.description != description:
            dictionary.name = newName
            dictionary.description = description
            db.session.commit()
            return True

    def isExist(self, user, name):
        return True if self.get(user, name) else False

    def addWord(self, user, name, original, translate,
                transcription, time, replace):
        dictionary = self.get(user, name)

        if self._word.isExist(dictionary, original):
            self._word.change(dictionary, original, original, translate,
                              transcription, time, replace)
        else:
            self._word.add(dictionary, original, translate,
                           transcription, time)
        return True

    def deleteWord(self, user, name, original):
        dictionary = self.get(user, name)
        if self._word.isExist(dictionary, original):
            self._word.delete(dictionary, original)
            return True
        else:
            raise WordNotExistError

    def changeWord(self, user, name, old, new,
                   translate, transcription, time):
        dictionary = self.get(user, name)

        if self._word.isExist(dictionary, old):
            self._word.change(dictionary, old, new, translate,
                              transcription, time, replace=True)
            return True
        else:
            raise WordNotExistError

    def word(self, user, word):
        # find word in all user's dictionaries
        # word may be as a original, as a translate
        for dict_ in self.all(user):
            for word_ in self._word.all(dict_):
                if word in (word_.original, word_.translate):
                    return word_
        return None

    def words(self, user, name):
        # List all objects "Word" of this dictionary
        dictionary = self.get(user, name)
        words = list()

        for word in self._word.all(dictionary):
            words.append({'original': word.original,
                          'translate': word.translate,
                          'transcription': word.transcription,
                          'updateTime': word.updateTime})
        return words

    def allWords(self, user):
        dicts = self.all(user)
        allWords = list()

        for dict_ in dicts:
            allWords.extend(self.words(user, dict_.name))

        return allWords

    def search(self, user, find):
        dicts = self.all(user)
        found = list()

        for dict_ in dicts:
            found.extend(self._word.search(dict_, find))

        return found
