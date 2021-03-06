from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField,\
    SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Regexp, ValidationError
import app.consts as consts
from ..functions import trim


class WordBaseForm(FlaskForm):
    original = StringField(
        'Original',
        validators=[
            DataRequired(),
            Regexp(consts.regexp.EN,
                   message=consts.regexp.EN_MSG)
        ],
        render_kw={'placeholder': 'original'})

    dictionary = HiddenField()


class WordFullForm(WordBaseForm):
    translate = StringField(
        'Translate',
        validators=[
            DataRequired(),
            Regexp(consts.regexp.RU,
                   message=consts.regexp.RU_MSG)
        ],
        render_kw={'placeholder': 'translate'})

    transcription = StringField(
        'Transcription',
        render_kw={'placeholder': 'transcription'})

    replace = BooleanField(label='Replace')

    def validate_translate(self, translate):
        if not trim(translate.data):
            raise ValidationError('You did mistake in {}.'.
                                  format(translate.data))


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
