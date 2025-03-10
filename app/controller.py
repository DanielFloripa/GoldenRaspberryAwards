from sqlalchemy import func
from sqlalchemy.orm import aliased

from app.models import Movie
from app.extensions import db


class MovieController:
    def __init__(self):
        self.movies_data = None

    def get_all(self):
        if not self.movies_data:
            self.movies_data = Movie.query.all()
        return self.movies_data
    
    def get_movie(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        return movie.as_dict()
        
    def get_nominees(self):
        self.get_all()
        nominees = [
            movie.as_dict() for movie in self.movies_data if not movie.winner
        ]
        return nominees

    def get_winner(self):
        self.get_all()
        winners = [
            movie.as_dict() for movie in self.movies_data if movie.winner
        ]
        return winners
    
    def get_interval(self):
        # Alias for self-join
        MovieAlias = aliased(Movie)
        results = {}
        # Query to find the intervals between consecutive awards for each producer
        intervals_query = db.session.query(
            Movie.producers,
            Movie.year.label('previous_win'),
            MovieAlias.year.label('following_win'),
            func.abs(MovieAlias.year - Movie.year).label('interval')
        ).join(
            MovieAlias,
            (Movie.producers == MovieAlias.producers)
            & (Movie.winner == True)
            & (MovieAlias.winner == True)
            & (MovieAlias.year != Movie.year)
        ).subquery()
        
        for key in ('min', 'max'):
            agg_func = getattr(func, key)
            order_func = getattr(
                agg_func(intervals_query.c.interval),
                'asc' if key == 'min' else 'desc'
            )()
            
            subquery = db.session.query(
                agg_func(intervals_query.c.interval).label('evaluated_interval')
            ).group_by(
                intervals_query.c.producers
            ).order_by(
                order_func
            ).first()
            
            # If has no data:
            if subquery is None:
                results[key] = []
                continue
            # Query to find the producer with the maximum interval
            results_key = db.session.query(
                intervals_query.c.producers,
                intervals_query.c.previous_win,
                intervals_query.c.following_win,
                agg_func(intervals_query.c.interval).label('agg_interval')
            ).filter(
                intervals_query.c.interval == subquery.evaluated_interval
            ).group_by(
                intervals_query.c.producers
            ).order_by(
                order_func
            )
            
            results[key] = [
                {
                    'producer': row.producers,
                    'interval': row.agg_interval,
                    'previousWin': row.previous_win,
                    'followingWin': row.following_win
                } for row in  results_key
            ]

        return results
    
    def add_new(self, data):
        new_movie = Movie(
            year=data['year'],
            title=data['title'],
            studios=data['studios'],
            producers=data['producers'],
            winner=data['winner']
        )
        db.session.add(new_movie)
        db.session.commit()
        return new_movie.as_dict()
    
    def update(self, data, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        if 'year' in data:
            movie.year = data['year']
        if 'title' in data:
            movie.title = data['title']
        if 'studios' in data:
            movie.studios = data['studios']
        if 'producers' in data:
            movie.producers = data['producers']
        if 'winner' in data:
            movie.winner = data['winner']
        db.session.commit()
        return movie.as_dict()
    
    def delete(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()
