from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, SelectField


class WordBaseForm(FlaskForm):
    original = StringField(render_kw={
        'value': '',
        'placeholder': 'original',
        'required': 'True',
        'pattern': '^[a-zA-Z\s]+$'})

    dictionary = HiddenField()


class WordFullForm(WordBaseForm):
    translate = StringField(render_kw={
        'value': '',
        'placeholder': 'translate',
        'required': 'True',
        'pattern': '^[А-Яа-яЁё\s]+$'})

    transcription = StringField(render_kw={
        'value': '',
        'placeholder': 'transcription'})


class AddWordForm(WordFullForm):
    def makeDictSelectField(self):
            AddWordForm.dictionary = SelectField()
    addWord = SubmitField('Add word')


class ChangeWordForm(WordFullForm):
    old = HiddenField()
    changeWord = SubmitField('Change word')


class DeleteWordForm(WordBaseForm):
    original = HiddenField()
    deleteWord = SubmitField('Delete word')

# class AddDictionaryForm(FlaskForm):
