import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommended_movies(user_id, user_ratings_df, min_rating=4.0, top_n=10):

    movies_df = pd.read_csv("movies.csv")
    
    # Kullanıcının yüksek puan verdiği filmleri filtrele
    high_rated = user_ratings_df[(user_ratings_df['userId'] == user_id) & (user_ratings_df['rating'] >= min_rating)]
    
    # Kullanıcının yüksek puan verdiği filmlerin türlerini almak
    movie_genres = movies_df[movies_df['movieId'].isin(high_rated['movieId'])]['genres']
    
    # TF-IDF Vektörizasyonu
    tfidf_vectorizer = TfidfVectorizer(token_pattern=r'[^\|]+')
    tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['genres'])
    
    # Kullanıcının yüksek puan verdiği filmlerin TF-IDF vektörlerini hesaplama
    user_tfidf = tfidf_vectorizer.transform(movie_genres)
    
    # Diğer tüm film vektörleri ile kozin benzerliği hesaplama
    cosine_sim_user = cosine_similarity(user_tfidf, tfidf_matrix)
    
    # Her film için en yüksek benzerlik skorlarına sahip filmleri bulma
    top_indices = np.argsort(cosine_sim_user, axis=1)[:, -top_n:]
    
    # Benzersiz öneri film ID'lerini al
    recommended_indices = np.unique(top_indices.flatten())
    recommended_movies = movies_df.iloc[recommended_indices]['movieId']
    
    # take only random 10
    recommended_movies = recommended_movies.sample(10)
    
    return recommended_movies.tolist()