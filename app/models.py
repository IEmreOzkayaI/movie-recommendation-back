from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'production_year': self.production_year,
            'categories': ', '.join([category.name for category in self.categories]),
            'overview': self.overview,
            'vote_average': self.vote_average,
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
    
    def __repr__(self):
        return f'{self.name} category'
    
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie', backref=db.backref('ratings', lazy=True))
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    
    def serialize(self):
        return {
            'id': self.id,
            'movie': self.movie.serialize(),
            'rating': self.rating,
            'user': self.user.serialize()
        }
    
    def __repr__(self):
        return f'{self.user.email} rated {self.movie.title} with {self.rating}'