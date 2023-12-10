"""Define site forms"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    """Define category form"""

    edit = StringField("Edit")
    title = StringField("Title", validators=[DataRequired()])
    parent = SelectField("Parent", choices=[("None", "-")])
    index = IntegerField("Index")
    submit = SubmitField("Add")


class ArticleForm(FlaskForm):
    """Define article form"""

    title = StringField("Title", validators=[DataRequired()])
    category = SelectField("category", choices=[("None", "-")], id="category")
    sub_category = SelectField(
        "Sub Category", choices=[("None", "-")], id="sub-category"
    )
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
