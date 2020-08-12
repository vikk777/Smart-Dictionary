from app import db
from .word_model import WordModel


class Word():
    """Class-decorator upon database.WordModel"""

    def add(self, dictionary, original, translate,
            transcription, time):
        word = WordModel(dictionary=dictionary, original=original.lower(),
                         translate=translate.lower(),
                         transcription=transcription,
                         updateTime=time)
        db.session.add(word)
        db.session.commit()
        return True

    def all(self, dictionary):
        return WordModel.query.filter_by(
            dictionary=dictionary).order_by(WordModel.updateTime).all()

    def get(self, dictionary, original):
        return WordModel.query.filter_by(dictionary=dictionary,
                                         original=original).first()

    def delete(self, dictionary, original):
        word = self.get(dictionary, original)
        db.session.delete(word)
        db.session.commit()
        return True

    def change(self, dictionary, old, new, translate,
               transcription, time, replace):
        word = self.get(dictionary, old)
        word.updateTime = time

        if old != new:
            word.original = new

        if replace:
            word.translate = translate
        else:
            translates = word.translate.split(', ')

            for item in translate.split(', '):
                if item not in translates:
                    word.translate += ', ' + item

        if transcription:
            word.transcription = transcription

        db.session.commit()
        return True

    def isExist(self, dictionary, original):
        return True if self.get(dictionary, original) else False

    def search(self, dictionary, find):
        return WordModel.query.filter(
            (WordModel.original.like(f"%{find}%") | WordModel.translate.
                like(f"%{find}%")),
            WordModel.dictionary == dictionary
        ).all()
