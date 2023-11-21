"""Define site database"""
from site_packge import db


class Tutorial(db.Model):
    """Define tutorial table that contains site Tutorials (html, css, js,...)"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    Sections = db.relationship("Section", backref="tutorial", lazy=True)


class Section(db.Model):
    """Define tutorials sections table (html bascis, html forms, ...)"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    tutorial_id = db.Column(db.Integer, db.ForeignKey("tutorial.id"), nullable=False)


class Article(db.Model):
    """Define Article table that contains the content"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey("section.id"), nullable=False)