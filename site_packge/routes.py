"""Contains all the site routes"""
from flask import render_template, redirect, flash, url_for, jsonify, request
from site_packge import app, db
from site_packge.models import Category, SubCategory, Article
from site_packge.forms import CategoryForm, ArticleForm


def get_navigation() -> dict:
    """Get navigation menu data"""
    navigation = {}

    for item in Category.query.order_by(Category.id).all():
        first_section = SubCategory.query.filter(
            SubCategory.category_id == item.id
        ).first()

        if first_section is None:
            continue

        first_aricle = Article.query.filter(
            Article.sub_category_id == first_section.id
        ).first()

        if first_aricle is None:
            continue

        navigation[item.title] = {
            "category_id": item.id,
            "article_id": first_aricle.id,
        }

    return navigation


@app.route("/")
@app.route("/home", strict_slashes=False)
def home() -> str:
    """Home page route"""
    navigation = get_navigation()

    return render_template("index.html", title="Home", navigation=navigation)


@app.route("/create_category", methods=["POST", "GET"], strict_slashes=False)
def create_category():
    """Create categories route"""
    form = CategoryForm()

    navigation = get_navigation()
    categories = [
        (item.id, item.title) for item in Category.query.order_by(Category.id).all()
    ]
    sub_categories = [
        (item.title, item.category.title, item.index)
        for item in SubCategory.query.order_by(SubCategory.id, SubCategory.index).all()
    ]

    for category in categories:
        form.parent.choices.append(category)

    if form.validate_on_submit():
        if form.parent.data == "None":
            record = Category(title=form.title.data)
        else:
            index = (
                SubCategory.query.filter(
                    SubCategory.category_id == form.parent.data
                ).count()
                + 1
            )
            record = SubCategory(
                title=form.title.data, category_id=form.parent.data, index=index
            )

        db.session.add(record)
        db.session.commit()
        flash("Section has been created", "success")
        return redirect(url_for("home"))

    return render_template(
        "create_category.html",
        title="Create Section",
        navigation=navigation,
        form=form,
        categories=categories,
        sub_categories=sub_categories,
    )


@app.route("/create_article", methods=["POST", "GET"], strict_slashes=False)
def create_article():
    """Post page route"""
    form = ArticleForm()
    navigation = get_navigation()

    categories = [
        (item.id, item.title) for item in Category.query.order_by(Category.id).all()
    ]
    for category in categories:
        form.category.choices.append(category)

    if request.method == "POST":
        article = Article(
            title=form.title.data,
            content=form.content.data,
            sub_category_id=form.sub_category.data,
        )

        db.session.add(article)
        db.session.commit()
        flash("Post has been created!", "succes")
        return redirect(url_for("home"))

    return render_template(
        "create_article.html", title="Create Article", navigation=navigation, form=form
    )


@app.route(
    "/api/v1.0/sections/<int:parent_id>", methods=["POST", "GET"], strict_slashes=False
)
def get_sub_categories(parent_id):
    """Api to get all sub categories from category id"""
    sub_categories = SubCategory.query.filter(
        SubCategory.category_id == parent_id
    ).all()

    matched_categories = []

    for sub_category in sub_categories:
        matched_categories.append((sub_category.id, sub_category.title))

    return jsonify(matched_categories)


@app.route(
    "/api/v1.0/article/<int:article_id>", methods=["POST", "GET"], strict_slashes=False
)
def get_article(article_id):
    """Api to get an article from its id"""
    content = Article.query.filter(Article.id == article_id).first().content

    return content


@app.route("/api/v1.0/image", methods=["POST", "GET"], strict_slashes=False)
def get_image():
    """Api to get local image"""
    return url_for("static", filename=request.get_data().decode("utf-8"))


@app.route("/article/<int:category_id>/<int:article_id>", strict_slashes=False)
def article(category_id, article_id):
    """Define Article page"""
    navigation = get_navigation()
    sub_categories = SubCategory.query.filter(
        SubCategory.category_id == category_id
    ).all()

    side_data = {}

    for sub_category in sub_categories:
        side_data[sub_category.title] = []
        articles = Article.query.filter(
            Article.sub_category_id == sub_category.id
        ).all()
        for post in articles:
            side_data.get(sub_category.title).append((post.title, post.id))

    return render_template(
        "article.html",
        title="Article",
        navigation=navigation,
        category_id=category_id,
        side_data=side_data,
    )
