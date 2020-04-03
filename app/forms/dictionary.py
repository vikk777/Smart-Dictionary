from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Regexp


class DictionaryBaseForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Regexp('^[a-zA-Zа-яА-ЯёЁ\s]+$',
                   message='Latin and russian letters and spaces only.')
        ],
        render_kw={
            'placeholder': 'Dictionary name'})


class DictionaryFullForm(DictionaryBaseForm):
    description = StringField(
        'Description',
        validators=[
            Regexp('^[a-zA-Zа-яА-ЯёЁ\s]+$',
                   message='Latin and russian letters and spaces only.')
        ],
        render_kw={
            'placeholder': 'Dictionary description'})


class AddDictionaryForm(DictionaryFullForm):
    addDict = SubmitField('Create dictionary')


class ChangeDictionaryForm(DictionaryFullForm):
    old = HiddenField()
    changeDict = SubmitField('Change dictionary')


class DeleteDictionaryForm(DictionaryBaseForm):
    name = HiddenField()
    deleteDict = SubmitField('Delete dictionary')
