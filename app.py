from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
    key_points = db.Column(db.Text, nullable=False)
    post = db.Column(db.Text, nullable=True)
    review = db.Column(db.Text, nullable=True)

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
    key_points = request.form["key_points"]

    # Create a new article

    article = Article(topic=topic, length=length, key_points=key_points)
    db.session.add(article)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    article = Article.query.get_or_404(id)
    if request.method == "POST":
        article.topic = request.form["topic"]
        article.length = int(request.form["length"])
        article.key_points = request.form["key_points"]

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit.html", article=article)


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
