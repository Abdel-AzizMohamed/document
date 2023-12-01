"""Contains all the site routes"""
from flask import render_template, redirect, flash, url_for, jsonify, request
from site_packge import app, db
from site_packge.models import Tutorial, Section, Article
from site_packge.forms import SectionForm, PostForm


def get_navigation() -> dict:
    """Get navigation menu data"""
    navigation = {}

    for item in Tutorial.query.order_by(Tutorial.id).all():
        first_section = Section.query.filter(Section.tutorial_id == item.id).first()

        if first_section is None:
            continue

        first_aricle = Article.query.filter(
            Article.section_id == first_section.id
        ).first()

        if first_aricle is None:
            continue

        navigation[item.title] = {"tutorial_id": item.id, "article_id": first_aricle.id}

    return navigation


@app.route("/")
@app.route("/home", strict_slashes=False)
def home():
    """Home page route"""
    navigation = get_navigation()

    return render_template("index.html", title="Home", navigation=navigation)


@app.route("/create_section", methods=["POST", "GET"], strict_slashes=False)
def category():
    """Create Sections route"""
    form = SectionForm()

    navigation = get_navigation()
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


@app.route("/create_post", methods=["POST", "GET"], strict_slashes=False)
def create_post():
    """Post page route"""
    form = PostForm()
    navigation = get_navigation()

    tutorials = [
        (item.id, item.title) for item in Tutorial.query.order_by(Tutorial.id).all()
    ]
    for option in tutorials:
        form.tutorial.choices.append(option)

    print(form.section.data)

    if request.method == "POST":
        article = Article(
            title=form.title.data,
            content=form.content.data,
            section_id=form.section.data,
        )

        db.session.add(article)
        db.session.commit()
        flash("Post has been created!", "succes")
        return redirect(url_for("home"))

    return render_template("post.html", title="Post", navigation=navigation, form=form)


@app.route(
    "/api/v1.0/sections/<int:parent_id>", methods=["POST", "GET"], strict_slashes=False
)
def get_sections(parent_id):
    """Api to get all sections from tutorial id"""
    sections = Section.query.filter(Section.tutorial_id == parent_id).all()

    sections_list = []

    for section in sections:
        sections_list.append((section.id, section.title))

    return jsonify(sections_list)


@app.route(
    "/api/v1.0/article/<int:article_id>", methods=["POST", "GET"], strict_slashes=False
)
def get_article(article_id):
    """Api to get an article from its id"""
    content = Article.query.filter(Article.id == article_id).first().content

    return content


@app.route("/article/<int:tutorial_id>/<int:article_id>", strict_slashes=False)
def article(tutorial_id, article_id):
    """Define Article page"""
    navigation = get_navigation()
    sections = Section.query.filter(Section.tutorial_id == tutorial_id).all()

    side_data = {}

    for section in sections:
        side_data[section.title] = []
        articles = Article.query.filter(Article.section_id == section.id).all()
        for post in articles:
            side_data.get(section.title).append((post.title, post.id))

    return render_template(
        "article.html",
        title="Article",
        navigation=navigation,
        tutorial_id=tutorial_id,
        side_data=side_data,
    )
