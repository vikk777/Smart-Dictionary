from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Regexp


class WordBaseForm(FlaskForm):
    original = StringField(
        'Original',
        validators=[
            DataRequired(),
            Regexp('^[a-zA-Z\s]+$',
                   message='Latin letters and spaces only.')
        ],
        render_kw={'placeholder': 'original'})

    dictionary = HiddenField()


class WordFullForm(WordBaseForm):
    translate = StringField(
        'Translate',
        validators=[
            DataRequired(),
            Regexp('^[А-Яа-яЁё\s]+$',
                   message='Russian letters and spaces only.')
        ],
        render_kw={'placeholder': 'translate'})

    transcription = StringField(
        'Transcription',
        render_kw={'placeholder': 'transcription'})

    replace = BooleanField(label='Replace')


class AddWordForm(WordFullForm):
    addWord = SubmitField('Add word')


class AddWordSelectForm(AddWordForm):
    dictionary = SelectField()


class ChangeWordForm(WordFullForm):
    old = HiddenField()
    changeWord = SubmitField('Change word')


class DeleteWordForm(WordBaseForm):
    original = HiddenField()
    deleteWord = SubmitField('Delete word')
