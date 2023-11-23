"""Contains all the site routes"""
from flask import render_template, redirect, flash, url_for
from site_packge import app, db
from site_packge.models import Tutorial, Section, Article
from site_packge.forms import SectionForm


@app.route("/")
@app.route("/home", strict_slashes=False)
def home():
    """Home page route"""
    navigation = [item.title for item in Tutorial.query.order_by(Tutorial.id).all()]
    return render_template("index.html", title="Home", navigation=navigation)


@app.route("/create_section", methods=["POST", "GET"], strict_slashes=False)
def category():
    """Create Sections route"""
    form = SectionForm()

    navigation = [item.title for item in Tutorial.query.order_by(Tutorial.id).all()]
    tutorials = [
        (item.id, item.title) for item in Tutorial.query.order_by(Tutorial.id).all()
    ]
    sections = [
        (item.title, item.tutorial.title, item.index)
        for item in Section.query.order_by(Section.id, Section.index).all()
    ]

    for option in tutorials:
        form.parent.choices.append(option)

    if form.validate_on_submit():
        if form.parent.data == "None":
            record = Tutorial(title=form.title.data)
        else:
            index = (
                Section.query.filter(Section.tutorial_id == form.parent.data).count()
                + 1
            )
            record = Section(
                title=form.title.data, tutorial_id=form.parent.data, index=index
            )

        db.session.add(record)
        db.session.commit()
        flash("Section has been created", "success")
        return redirect(url_for("home"))

    return render_template(
        "create_section.html",
        title="Create Section",
        navigation=navigation,
        form=form,
        tutorials=tutorials,
        sections=sections,
    )
