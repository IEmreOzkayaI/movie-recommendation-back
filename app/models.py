import random
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Many-to-Many ilişki tablosu
movie_category = db.Table('movie_category',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    ratings = db.relationship('Rating', back_populates='user')

    def check_password(self, password):
        return self.password == password

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'surname': self.surname
        }

    def __repr__(self):
        return f'{self.email} user'

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=True)
    production_year = db.Column(db.Integer, nullable=True)
    overview = db.Column(db.String(1000), nullable=True)
    vote_average = db.Column(db.Float, nullable=True)
    poster_path = db.Column(db.String(120), nullable=True)
    categories = db.relationship('Category', secondary=movie_category, back_populates="movies")
    ratings = db.relationship('Rating', back_populates='movie')

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'production_year': self.production_year,
            'categories': ', '.join([category.name for category in self.categories]),
            'overview': self.overview,
            'vote_average': self.vote_average,
            'poster_path': self.poster_path,
        }

    def related_movies(self):
        all_other_movies = []
        for category in self.categories:
            other_movies = Movie.query.join(movie_category).filter(
                movie_category.c.category_id == category.id,
                Movie.id != self.id
            ).all()
            all_other_movies.extend(other_movies)

        unique_movies = list({movie.id: movie for movie in all_other_movies}.values())  # Duplicate filmleri kaldır

        if len(unique_movies) > 6:
            related_movies = random.sample(unique_movies, 6)
        else:
            related_movies = unique_movies
            while len(related_movies) < 6:
                extra_movies = random.sample(unique_movies, 6 - len(related_movies))
                related_movies.extend(extra_movies)
                related_movies = list({movie.id: movie for movie in related_movies}.values())  # Duplicate filmleri tekrar kaldır

        return {'related_movies': [movie.simple_serialize() for movie in related_movies]}


    def simple_serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'poster_path': self.poster_path
        }

    def pagination_serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'poster_path': self.poster_path
        }

    def __repr__(self):
        return f'{self.title} movie'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    movies = db.relationship('Movie', secondary=movie_category, back_populates="categories")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def concat_movies(self):
        return ', '.join([movie.title for movie in self.movies])

    def get_movies(self):
        return [movie.simple_serialize() for movie in self.movies]

    def __repr__(self):
        return f'{self.name} category'

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie', back_populates='ratings')
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='ratings')

    def serialize(self):
        return {
            'id': self.id,
            'movie': self.movie.id,
            'rating': self.rating,
            'user': self.user.id
        }

    def __repr__(self):
        return f'{self.user.email} rated {self.movie.title} with {self.rating}'
