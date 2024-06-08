from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from agents.writer import BlogWriterAgent, TopicGeneratorAgent

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog_writer.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# MODELS

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    post = db.Column(db.Text, nullable=True)
    niche = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Article({self.topic}, {self.length})"


with app.app_context():
    db.create_all()

# API ROUTES


@app.route("/")
def index():
    articles = Article.query.all()
    return render_template("index.html", articles=articles)


@app.route("/write", methods=["POST"])
def write():
    topic = request.form["topic"]
    length = int(request.form["length"])
    niche = request.form["niche"]

    # Create a new article
    article = Article(topic=topic, length=length, niche=niche)
    db.session.add(article)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    article = Article.query.get_or_404(id)
    if request.method == "POST":
        article.topic = request.form["topic"]
        article.length = int(request.form["length"])

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit.html", article=article)


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete_all", methods=["POST"])
def delete_all():
    try:
        # Delete all articles
        db.session.query(Article).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Handle the exception, possibly logging the error
        print(f"An error occurred while deleting articles: {e}")

    return redirect(url_for("index"))


@app.route("/generate/<int:id>", methods=["POST"])
def generate(id):
    article = Article.query.get_or_404(id)

    # Generate the blog post using BlogWriter
    writer = BlogWriterAgent(topic=article.topic, length=article.length)
    result = writer.generate()

    article.post = result

    db.session.commit()

    return jsonify(result)


@app.route("/generate_topics", methods=["POST"])
def generate_topics():
    niche = request.form["niche"]
    count = int(request.form["count"])

    # Let agent work

    agent = TopicGeneratorAgent(
        niche=niche, count=count
    )

    result: list[str] = agent.generate()

    for topic in result:
        # Create a new article
        article = Article(topic=topic, length=200, niche=niche)
        db.session.add(article)
        db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
