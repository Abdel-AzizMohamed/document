"""Define site forms"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class SectionForm(FlaskForm):
    """Define create section form"""
    edit = StringField("Edit")
    title = StringField("Title", validators=[DataRequired()])
    parent = SelectField("Parent", choices=[("None", "-")])
    index = IntegerField("Index")
    submit = SubmitField("Add")
