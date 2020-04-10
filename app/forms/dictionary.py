from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Regexp
import app.consts as consts


class DictionaryBaseForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Regexp(consts.regexp.RU_EN_FULL,
                   message=consts.regexp.RU_EN_MSG)
        ],
        render_kw={
            'placeholder': 'Dictionary name'})


class DictionaryFullForm(DictionaryBaseForm):
    description = StringField(
        'Description',
        validators=[
            Regexp(consts.regexp.RU_EN_EMPTY,
                   message=consts.regexp.RU_EN_MSG)
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
