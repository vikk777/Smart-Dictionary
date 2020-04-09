from flask_wtf import FlaskForm
from wtforms import Form, FormField, FieldList, StringField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Regexp


class TestStartForm(FlaskForm):
    dictionary = SelectField()
    period = SelectField()
    startTest = SubmitField('Start test')


class TestNextForm(FlaskForm):
    question = HiddenField()
    answer = StringField(
        validators=[DataRequired()],
        render_kw={
            'autofocus': True})
    nextQuestion = SubmitField('Next')


class CorrectMistakesForm(FlaskForm):
    correctMistakes = SubmitField('Correct the mistakes')
