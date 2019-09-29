from middle import db


# class Article(db.Model):
#     __tablename__ = 'article'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     # tags = db.Column(db.String(100), nullable=False)


class Top100(db.Model):
    __tablename__ = "top_100"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ranking = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False, unique=True)
    stars = db.Column(db.String(255), nullable=False)
    release_time = db.Column(db.String(255), nullable=False)
    score = db.Column(db.DECIMAL(10, 4), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
