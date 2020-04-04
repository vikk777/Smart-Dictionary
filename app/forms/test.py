from flask_wtf import FlaskForm
from wtforms import Form, FormField, FieldList, StringField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Regexp


class TestStartForm(FlaskForm):
    startTest = SubmitField('Start test')
    dictionary = SelectField()


class TestFinishForm(FlaskForm):
    answers = FieldList(StringField(validators=[DataRequired()]))
    # questions = FieldList(HiddenField())
    finishTest = SubmitField('Finish test')
