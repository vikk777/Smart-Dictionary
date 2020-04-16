from app import db
import app.database as tables


class Dictionary():
    """Class-decorator upon database.Dictionaries"""

    def __init__(self, name, description):
        # self._name = name
        # self._description = description
        # self._words = dict()
        d = tables.Dictionary(name=name, description=description)
        db.session.add(d)
        db.session.commit()

    def setName(self, oldName, newName):
        # self._name = name
        d = db.session.query(tables.Dictionary).filter_by(name=oldName)
        d.name = newName

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
        if word.original() in self._words:
            del self._words[word.original()]

        self._words[word.original()] = word

    def deleteWord(self, word):
        del self._words[word]

    def changeWord(self, old, new):
        if old != new.original():
            del self._words[old]

        self.addWord(new)
