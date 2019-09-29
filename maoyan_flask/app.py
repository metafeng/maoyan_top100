from flask import Flask, render_template, url_for, request
from middle import db
from models import Top100

import function_tools as ft

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
        page_title = "Maoyan Top100"

    return render_template("index.html", page_title=page_title)


@app.route('/events/')
def events():
    page_title = "Events"
    return render_template("event.html", page_title=page_title)


@app.route('/load_more_movies/', methods=['GET', 'POST'])
def load_more_movies():
    print(request.values)
    page = request.values.get('page')
    off_set = int(page) * 12
    load_more_list = ft.format_to_list(
        Top100.query.offset(off_set).limit(12).all())
    return ft.list_to_json(load_more_list)


@app.route('/login/')
def ligon():
    page_title = 'login'
    return render_template('login.html', page_title=page_title)


@app.context_processor
def my_context_processor():
    context_dict = {}
    context_dict['movies_list'] = ft.format_to_list(
        Top100.query.offset(0).limit(12).all())
    context_dict['order_by_score'] = \
        ft.format_to_list(Top100.query.order_by(db.desc('score')).all())
    context_dict['order_by_time'] = \
        ft.format_to_list(Top100.query.order_by(db.desc('release_time')).all())
    if context_dict:
        return context_dict
    else:
        return {}


if __name__ == '__main__':
    app.run(port='80')
