from .controllers import home, login, register, movie, rating,movies,recommendation
from .auth import token_required

def register_routes(app):
    app.add_url_rule('/health', view_func=home, methods=['GET'])
    app.add_url_rule('/login', view_func=login, methods=['POST'])
    app.add_url_rule('/register', view_func=register, methods=['POST'])
    
    app.add_url_rule('/movies', view_func=movies, methods=['GET'])
    app.add_url_rule('/movie', view_func=token_required(movie), methods=['GET'])
    app.add_url_rule('/recommendation', view_func=token_required(recommendation), methods=['GET'])
    
    
    app.add_url_rule('/rating', view_func=token_required(rating), methods=['POST'])
    
    


