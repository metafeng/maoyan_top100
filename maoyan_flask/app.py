from flask import Flask, render_template, url_for, request
from flask import g, redirect, session, flash
from middle import db
from models import Top100, User
from extension import format_to_list, list_to_json, validate
from decorators import login_required
import json


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


@app.route('/')
def index():
    movies = Top100.query.all()
    movies_list = []
    for movie in movies:
        movie_dict = dict(
            ranking=movie.ranking,
            title=movie.title,
            stars=movie.stars,
            release_time=movie.release_time,
            score=movie.score,
            img_url=movie.img_url,
        )
        movies_list.append(movie_dict)
    context = dict(
        page_title='Maoyan Top100',
    )

    return render_template('index.html', **context)


@app.route('/events/')
def events():
    context = dict(
        page_title='Events',
    )

    return render_template('event.html', **context)


@app.route('/load_more_movies/', methods=['GET', 'POST'])
def load_more_movies():
    page = request.values.get('page')
    off_set = int(page) * 12
    load_more_list = format_to_list(
        Top100.query.offset(off_set).limit(12).all())
    return list_to_json(load_more_list)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == "POST":
        print(request.form)
        email = request.form.get("email")
        password1 = request.form.get("password")
        user_query = User.query.filter(User.email == email).first()
        message = validate(user_query, email, password1)

        if message == 'success':
            session['user_id'] = user_query.id
            session['user_name'] = user_query.username
            session.permenet = True
            return dict(status='success', message=url_for("events"))
        else:
            return dict(message=message)

    else:
        context = dict(
            page_title='Login',
        )

        return render_template('login.html', **context)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        print(request.form)
        username = request.form.get('username')
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user_query = User.query.filter(User.email == email).first()
        message = validate(user_query, email, password1, password2, username)

        if message == 'success':
            user_new = User(username=username, email=email, password='p123456')
            db.session.add(user_new)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            flash(message)

    context = dict(
        page_title='Register',
    )

    return render_template('register.html', **context)


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    print(request.form)
    context = dict(
        page_title='Contact',
    )

    return render_template('contact.html', **context)


@app.route("/blog/")
@login_required
def blog():
    context = dict(
        page_title='Blog',
    )
    return render_template('blog.html', **context)


@app.route('/movies/')
def movies():
    context = dict(
        page_title='Movies',
    )

    return render_template('movies.html', **context)


@app.before_request
def my_before_request():
    if session.get("user_name"):
        g.user_name = session.get('user_name')


@app.context_processor
def my_context_processor():
    context_dict = {}
    context_dict['movies_list'] = format_to_list(
        Top100.query.offset(0).limit(12).all())
    context_dict['order_by_score'] = \
        format_to_list(Top100.query.order_by(db.desc('score')).all())
    context_dict['order_by_time'] = \
        format_to_list(Top100.query.order_by(db.desc('release_time')).all())
    if hasattr(g, 'user_name'):
        context_dict['user_name'] = g.user_name
    if context_dict:
        return context_dict
    else:
        return {}


if __name__ == '__main__':
    app.run(port='80')
