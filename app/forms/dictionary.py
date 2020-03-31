from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, SelectField


class DictionaryBaseForm(FlaskForm):
    name = StringField(render_kw={
        'placeholder': 'Dictionary name',
        'required': 'True',
        'pattern': '^[a-zA-Z\s]+$'})


class DictionaryFullForm(DictionaryBaseForm):
    description = StringField(render_kw={
        'placeholder': 'Dictionary description',
        'required': 'True',
        'pattern': '^[a-zA-Z\s]+$'})


class AddDictionaryForm(DictionaryFullForm):
    addDict = SubmitField('Create dictionary')


class ChangeDictionaryForm(DictionaryFullForm):
    old = HiddenField()
    changeDict = SubmitField('Change dictionary')


class DeleteDictionaryForm(DictionaryBaseForm):
    name = HiddenField()
    deleteDict = SubmitField('Delete dictionary')
