from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class ImportForm(FlaskForm):
    words = TextAreaField(
        validators=[DataRequired()],
        render_kw={
            'rows': '10',
            'placeholder': 'Example: hello - привет, здравствуйте'})
    dictionary = SelectField()
    importWords = SubmitField('Import')
