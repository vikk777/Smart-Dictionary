from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired


class TestStartForm(FlaskForm):
    dictionary = SelectField()
    period = SelectField()
    startTest = SubmitField('Start test')


class TestNextForm(FlaskForm):
    question = HiddenField(validators=[DataRequired()])
    answer = StringField(
        validators=[DataRequired()],
        render_kw={
            'autofocus': True})
    nextQuestion = SubmitField('Next')


class CorrectMistakesForm(FlaskForm):
    correctMistakes = SubmitField('Correct the mistakes')
