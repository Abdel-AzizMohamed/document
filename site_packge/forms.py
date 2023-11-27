"""Define site forms"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class SectionForm(FlaskForm):
    """Define create section form"""

    edit = StringField("Edit")
    title = StringField("Title", validators=[DataRequired()])
    parent = SelectField("Parent", choices=[("None", "-")])
    index = IntegerField("Index")
    submit = SubmitField("Add")


class PostForm(FlaskForm):
    """Define create post form"""

    title = StringField("Title", validators=[DataRequired()])
    tutorial = SelectField("tutorial", choices=[("None", "-")], id="category")
    section = SelectField("section", choices=[("None", "-")], id="sub-category")
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
