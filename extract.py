import pandas as pd

# # Veriyi yükleyelim
# movies_df = pd.read_csv('movies.csv')  # Dosya yolu 'movies.csv' olduğunu varsayıyorum

# # 'genres' sütunundaki null değerleri filtreleyelim
# movies_df = movies_df.dropna(subset=['genres'])

# # 'genres' sütununu '|' ile ayırıp, düzleştirerek benzersiz kategorileri bulalım
# movies_df['genres'] = movies_df['genres'].apply(lambda x: x.split('|'))
# unique_genres = set(genre for sublist in movies_df['genres'] for genre in sublist)

# # Benzersiz kategorileri sıralayalım ve ekrana yazdıralım
# sorted_unique_genres = sorted(unique_genres)
# print(sorted_unique_genres[0])

# # Benzersiz kategorilerin sayısını yazdıralım
# print("Total number of unique genres:", len(sorted_unique_genres))

# import pandas as pd

# # Veriyi yükleyelim
# movies_df = pd.read_csv('movies.csv')

# # 'genres' sütununu ayırıp, her bir genre için yeni bir satır oluşturalım
# exploded_genres_df = movies_df.assign(genres=movies_df['genres'].str.split('|')).explode('genres')

# # Sonuçları gözlemleyelim
# print(exploded_genres_df.head())

# # Sonuçları bir CSV dosyasına kaydedelim veya doğrudan veritabanına yükleyelim
# exploded_genres_df.to_csv('exploded_genres_movies.csv', index=False)


# import pandas as pd

# # Veriyi yükleyelim
# movies_df = pd.read_csv('movies.csv')

# # 'genres' sütununu ayırıp, her bir genre için yeni bir satır oluşturalım
# exploded_genres_df = movies_df.assign(genres=movies_df['genres'].str.split('|')).explode('genres')

# # Genre isimlerini ID'leri ile eşleştiren bir sözlük
# genre_to_id = {
#     'Action': 1,
#     'Adventure': 2,
#     'Animation': 3,
#     'Children': 4,
#     'Comedy': 5,
#     'Crime': 6,
#     'Documentary': 7,
#     'Drama': 8,
#     'Fantasy': 9,
#     'Film-Noir': 10,
#     'Horror': 11,
#     'IMAX': 12,
#     'Musical': 13,
#     'Mystery': 14,
#     'Romance': 15,
#     'Sci-Fi': 16,
#     'Thriller': 17,
#     'War': 18,
#     'Western': 19,
#     '(no genres listed)': 20
# }

# # Genre isimlerini ID'ler ile değiştir
# exploded_genres_df['genre_id'] = exploded_genres_df['genres'].map(genre_to_id)

# # Sonuçları gözlemleyelim
# print(exploded_genres_df[['movieId', 'genre_id']])

# # Sonuçları bir CSV dosyasına kaydedelim
# exploded_genres_df[['movieId', 'genre_id']].to_csv('updated_genres_movies.csv', index=False)

# import pandas as pd
# import re

# # Veriyi yükleyelim
# df = pd.read_csv('exploded_genres_movies.csv')

# # 'genres' kolonunu dataframe'den silelim
# df.drop('genres', axis=1, inplace=True)

# # 'title' kolonundan yılı çıkarmak için bir regex kullanarak 'production_year' kolonu ekleyelim
# df['production_year'] = df['title'].str.extract(r'\((\d{4})\)')

# # 'title' kolonundan yılı silmek için regex kullanalım
# df['title'] = df['title'].str.replace(r'\s*\(\d{4}\)\s*', '', regex=True)

# # Sonuçları gözlemleyelim
# print(df.head())

# # Sonuçları bir CSV dosyasına kaydedelim
# df.to_csv('cleaned_movies.csv', index=False)


# import pandas as pd

# # Veriyi yükleyelim
# df = pd.read_csv('cleaned_movies.csv')

# # Tekrar eden satırları kaldıralım. `movieId` ve `genre_id` üzerinden benzersizlik sağlayalım
# df_unique = df.drop_duplicates(subset=['movieId', 'title','production_year'])

# # Sonuçları gözlemleyeli
# print(df_unique.head())

# # Sonuçları bir CSV dosyasına kaydedelim
# df_unique.to_csv('unique_movies.csv', index=False)


# INSERT INTO movie.category (name) VALUES 
# ('Action'),
# ('Adventure'),
# ('Animation'),
# ('Children'),
# ('Comedy'),
# ('Crime'),
# ('Documentary'),
# ('Drama'),
# ('Fantasy'),
# ('Film-Noir'),
# ('Horror'),
# ('IMAX'),
# ('Musical'),
# ('Mystery'),
# ('Romance'),
# ('Sci-Fi'),
# ('Thriller'),
# ('War'),
# ('Western'),
# ('(no genres listed)');


import pandas as pd

# Veriyi yükleyelim
df = pd.read_csv('unique_movies.csv')

# 'production_year' sütunundaki ondalık değerleri int türüne çevirerek yıl bilgisini güncelleyelim
df['production_year'] = df['production_year'].fillna(0).astype(int)

# Sonuçları gözlemleyelim
print(df.head())

# Sonuçları bir CSV dosyasına kaydedelim
df.to_csv('unique_movies_2.csv', index=False)
