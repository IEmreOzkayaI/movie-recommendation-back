import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# movies.csv okuma
movies_df = pd.read_csv("movies.csv")

# TF-IDF Vektörizasyonu
tfidf_vectorizer = TfidfVectorizer(token_pattern=r'[^\|]+')
tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['genres'])

# Örnek film ID'leri ve rastgele puanlar  
# TODO: bunu parametrik vericem, dataframe direkt sql den yap.
data = {
    'userId': [99999]*50,
    'movieId': np.random.randint(1, 300, size=50),
    'rating': np.random.uniform(2.5, 5.0, size=50)
}

user_ratings = pd.DataFrame(data)

# TODO: öncesinde filtreletip getirsek daha iyi.
high_rated = user_ratings[user_ratings['rating'] >= 4.0]

# Kullanıcının yüksek puan verdiği filmlerin türlerini almak
movie_genres = movies_df[movies_df['movieId'].isin(high_rated['movieId'])]['genres']

# TF-IDF vektörlerini hesaplama
user_tfidf = tfidf_vectorizer.transform(movie_genres)

# Diğer tüm film vektörleri ile kozin benzerliği hesaplama
cosine_sim_user = cosine_similarity(user_tfidf, tfidf_matrix)

# Her film için en yüksek benzerlik skorlarına sahip filmleri bulma
top_indices = np.argsort(cosine_sim_user, axis=1)[:, -10:]

# Benzersiz öneri film ID'lerini al
recommended_indices = np.unique(top_indices)
recommended_movies = movies_df.loc[recommended_indices, ['movieId']]
list_of_movies = recommended_movies['movieId'].tolist()

print("\nÖnerilen Filmler:")
print(list_of_movies)