from app import app, db
from app.model.word_model import WordModel
from app.model.dictionary_model import DictionaryModel
from app.model.user_model import UserModel, mistakesTable


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'word': WordModel,
            'dictionary': DictionaryModel,
            'user': UserModel,
            'mistakes': mistakesTable}


if __name__ == '__main__':
    app.run()
