# import pandas as pd
# import requests

# # CSV dosyasını yükle
# df = pd.read_csv('cleaned_unique_movies_2.csv')

# # API ile ilgili ayarlar
# api_url = "https://api.themoviedb.org/3/search/movie"
# params = {
#     'include_adult': 'false',
#     'language': 'en-US',
#     'page': 1
# }
# headers = {
#     'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZjgzZmJhMDI5MTQyYmE5YTZlMWU4NmVjYzA5OTcyMCIsInN1YiI6IjY1ZmQ2M2QzNjA2MjBhMDE3YzI5ODg3NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Rl4mu720ZHYLYZOZFimFf5KHA27lkP8MU-iP4_S4JBc',
#     'Content-Type': 'application/json;charset=utf-8'
# }
# base_image_url = "https://image.tmdb.org/t/p/original"

# # Filmleri sırayla işle
# for index, row in df.iterrows():
#     movie_name = row['title']
#     params['query'] = movie_name
#     response = requests.get(api_url, headers=headers, params=params)
#     print(f"Processing {index + 1}/{len(df)}: {movie_name}")  # İşlem logu
#     if response.status_code == 200:
#         data = response.json()
#         results = data.get('results', [])
#         if results:
#             first_result = results[0]
#             # İstenen bilgileri çek
#             poster_path = first_result.get('poster_path', '')
#             overview = first_result.get('overview', '')
#             vote_average = first_result.get('vote_average', '')
            
#             full_poster_path = f"{base_image_url}{poster_path}" if poster_path else ''
            
#             # DataFrame'e yeni verileri ekle
#             df.at[index, 'poster_path'] = full_poster_path
#             df.at[index, 'overview'] = overview
#             df.at[index, 'vote_activity'] = vote_average
#         else:
#             print(f"No results found for {movie_name}")
#     else:
#         print(f"Error fetching data for {movie_name}: {response.status_code}")

# # Güncellenmiş DataFrame'i kaydet
# df.to_csv('updated_cleaned_unique_movies_2.csv', index=False)


# import pandas as pd

# # CSV dosyasını yükle
# df = pd.read_csv('unique_movies_2.csv')

# # title'daki parantezleri ve içindekileri kaldır
# df['title'] = df['title'].str.replace(r"\s*\([^)]*\)", "", regex=True)

# # Güncellenmiş DataFrame'i kaydet
# df.to_csv('cleaned_unique_movies_2.csv', index=False)

# # İlk birkaç satırı göstererek sonuçları kontrol et
# print(df.head())



import pandas as pd
import requests

# API ile ilgili ayarlar
api_url = "https://api.themoviedb.org/3/search/movie"
params = {
    'include_adult': 'false',
    'language': 'en-US',
    'page': 1
}
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZjgzZmJhMDI5MTQyYmE5YTZlMWU4NmVjYzA5OTcyMCIsInN1YiI6IjY1ZmQ2M2QzNjA2MjBhMDE3YzI5ODg3NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Rl4mu720ZHYLYZOZFimFf5KHA27lkP8MU-iP4_S4JBc',
    'Content-Type': 'application/json;charset=utf-8'
}
base_image_url = "https://image.tmdb.org/t/p/original"

chunk_size = 100
input_filename = 'cleaned_unique_movies_2.csv'
output_filename = 'updated_cleaned_unique_movies_3.csv'
dff = pd.read_csv(input_filename)

# 100'lik parçalar halinde işle
for start in range(0, len(dff), chunk_size):
    # Veriyi parça parça oku
    df = pd.read_csv(input_filename, skiprows=range(1, start+1), nrows=chunk_size, header=0)
    
    # Filmleri sırayla işle
    for index, row in df.iterrows():
        real_index = start + index
        movie_name = row['title']
        params['query'] = movie_name
        response = requests.get(api_url, headers=headers, params=params)
        print(f"Processing {real_index + 1}/{len(dff)}: {movie_name}")  # İşlem logu
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            if results:
                first_result = results[0]
                # İstenen bilgileri çek
                poster_path = first_result.get('poster_path', '')
                overview = first_result.get('overview', '')
                vote_average = first_result.get('vote_average', '')
                full_poster_path = f"{base_image_url}{poster_path}" if poster_path else ''
                
                # DataFrame'e yeni verileri ekle
                df.at[index, 'poster_path'] = full_poster_path
                df.at[index, 'overview'] = overview
                df.at[index, 'vote_average'] = vote_average
            else:
                print(f"No results found for {movie_name}")
        else:
            print(f"Error fetching data for {movie_name}: {response.status_code}")

    # İşlenen parçayı farklı bir dosyaya kaydet
    if start == 0:
        df.to_csv(output_filename, mode='w', index=False, header=True)  # İlk parça, header ile birlikte yaz
    else:
        df.to_csv(output_filename, mode='a', index=False, header=False)  # Diğer parçalar, header olmadan ekle

