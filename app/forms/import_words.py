from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Regexp


class ImportForm(FlaskForm):
    words = TextAreaField(
        validators=[DataRequired()],
        # Regexp(
        #     '^[a-zA-ZА-Яа-яЁё\s,-]+$',
        #     message='Latin and russian letters, commas, dash and spaces only.')],
        render_kw={
            'cols': '70',
            'rows': '20',
            'placeholder': 'Example: hello - привет, здравствуйте'})
    dictionary = SelectField()
    importWords = SubmitField('Import')
