from flask_wtf import FlaskForm
from wtforms import StringField  # , SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    word = StringField(
        'Search',
        validators=[
            DataRequired()],
        render_kw={'placeholder': 'Alt+S'})
    # search=SubmitField())
