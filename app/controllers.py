import jwt
import datetime
from flask import request, jsonify
from .models import User, db, Movie , Rating, Category
from flask import current_app as app  # Assuming the Flask app is imported as 'app' in your models

def home():
    return "Hello, World!"

def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'All fields are required'}), 400
        
        # Assuming password is stored in hashed form and User model has a method to check password
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):  # Assuming you have a method to check hashed password
            # Create a token
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expires in 24 hours
            }, app.config['SECRET_KEY'], algorithm="HS256")  # Ensure you have a SECRET_KEY configured in your app's config

            return jsonify({'token': token ,"user":{ "name": user.name, "surname":user.surname, "id":user.id}}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Method not allowed'}), 405
    
def register():
    if request.method == 'POST':
        data = request.get_json()  # JSON verisini al
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        surname = data.get('surname')
        
        if not email or not password or not name or not surname:
            return jsonify({'message': 'All fields are required'}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'Email already exists'}), 409

        new_user = User(email=email, password=password, name=name, surname=surname)
        db.session.add(new_user)
        try:
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except:
            db.session.rollback()
            return jsonify({'message': 'Registration failed'}), 500
    return jsonify({'message': 'Method not allowed'}), 405

def movies():
    if request.method == 'GET':
        # Extract pagination parameters from the request query string
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=8, type=int)
        title = request.args.get('title')
        
        # Start building the base query
        base_query = Movie.query
        
        # Filter by title if provided
        if title:
            base_query = base_query.filter(Movie.title.like(f'%{title}%'))
        
        # Paginate the results
        movies_paginated = base_query.paginate(page=page, per_page=per_page)
        
        # Serialize the paginated movies and return as JSON response
        return jsonify({
            'movies': [movie.pagination_serialize() for movie in movies_paginated.items],
            'total_movies': movies_paginated.total,
            'current_page': movies_paginated.page,
            'per_page': movies_paginated.per_page,
            'has_next': movies_paginated.has_next,
            'has_prev': movies_paginated.has_prev
        }), 200

        # Paginate the results using the pagination parameters
        movies = Movie.query.paginate(page=page, per_page=per_page)

        # Serialize the paginated movies and return as JSON response
        return jsonify({
            'movies': [movie.pagination_serialize() for movie in movies.items],
            'total_movies': movies.total,
            'current_page': movies.page,
            'per_page': movies.per_page,
            'has_next': movies.has_next,
            'has_prev': movies.has_prev
        }), 200

    return jsonify({'message': 'Method not allowed'}), 405

    
def movie():
    if request.method == 'GET':
        movie_id = request.args.get('id')
        if not movie_id:
            return jsonify({'message': 'Movie ID is required'}), 400

        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({'message': 'Movie not found'}), 404

        return jsonify(movie.serialize()), 200
    
    return jsonify({'message': 'Method not allowed'}), 405

def rating():
    if request.method == 'POST':
        data = request.get_json()
        user = request.current_user
        movie_id = data.get('movie_id')
        rating = data.get('rating')

        if not movie_id or not rating:
            return jsonify({'message': 'All fields are required'}), 400

        new_rating = Rating(movie_id=movie_id, rating=rating, user=user)
        db.session.add(new_rating)
        try:
            db.session.commit()
            return jsonify({'message': 'Rating added successfully'}), 201
        except:
            db.session.rollback()
            return jsonify({'message': 'Rating failed'}), 500
        
    return jsonify({'message': 'Method not allowed'}), 405

        

    
