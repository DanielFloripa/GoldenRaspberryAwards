from flask import Flask, jsonify, request
from app.extensions import db
from app.models import Movie
from app.controller import MovieController


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

movie_controller = MovieController()

# Run once at startup
@app.before_request
def create_tables():
    if not hasattr(app, 'has_run'):
        db.create_all()
        Movie.load_movies_from_csv()
        app.has_run = True

@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify([movie.as_dict() for movie in movie_controller.get_all()])

@app.route('/nominees', methods=['GET'])
def get_nominees():
    return jsonify(movie_controller.get_nominees())

@app.route('/winners', methods=['GET'])
def get_winner():
    return jsonify(movie_controller.get_winner())

@app.route('/get_interval', methods=['GET'])
def get_interval():
    intervals = movie_controller.get_interval()
    return jsonify(intervals)

@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = movie_controller.get_movie(movie_id)
    return jsonify(movie), 200

@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    new_movie = movie_controller.add_new(data)
    return jsonify(new_movie), 201

@app.route('/movies/<int:movie_id>', methods=['PATCH'])
def update_movie(movie_id):
    data = request.get_json()
    movie = movie_controller.update(data, movie_id)
    return jsonify(movie)

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie_controller.delete(movie_id)
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
