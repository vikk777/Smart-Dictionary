from flask_wtf import FlaskForm
from wtforms import Form, FormField, FieldList, StringField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Regexp


class TestStartForm(FlaskForm):
    startTest = SubmitField('Start test')
    dictionary = SelectField()


class TestNextForm(FlaskForm):
    # answers = FieldList(StringField(validators=[DataRequired()]))
    # questions = FieldList(HiddenField())
    question = HiddenField()
    answers = StringField(validators=[DataRequired()])
    nextQuestion = SubmitField('Next')
