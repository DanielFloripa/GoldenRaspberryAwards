import csv
import os
from sqlalchemy import Column, Integer, String, Boolean
from app.extensions import db

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    studios = Column(String, nullable=True)
    producers = Column(String, nullable=True)
    winner = Column(Boolean, nullable=True)

    def __init__(self, year, title, studios, producers, winner):
        self.year = year
        self.title = title
        self.studios = studios
        self.producers = producers
        self.winner = str(winner).lower() in ('yes', 'true',)

    def __repr__(self):
        return f"<Movie {self.title} ({self.year})>"

    @classmethod
    def load_movies_from_csv(cls):
        db.create_all()
        csv_file_path = os.path.join(os.path.dirname(__file__), '../data/Movielist.csv')
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                movie = cls(
                    year=int(row['year']),
                    title=row['title'],
                    studios=row['studios'],
                    producers=row['producers'],
                    winner=row['winner']
                )
                db.session.add(movie)
            db.session.commit()
    
    def as_dict(self):
        return {
            'id': self.id,
            'year': self.year,
            'title': self.title,
            'studios': self.studios,
            'producers': self.producers,
            'winner': self.winner
        }