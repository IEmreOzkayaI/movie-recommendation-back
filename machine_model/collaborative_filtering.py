import os
from pyspark.sql import SparkSession, Row
from pyspark.ml.recommendation import ALS


def recommend_movies(new_user_id, new_user_ratings):
    # Aynı Python sürümünü kullanarak ortam değişkenlerini ayarlayın
    os.environ['PYSPARK_PYTHON'] = '/opt/anaconda3/bin/python3.11'
    os.environ['PYSPARK_DRIVER_PYTHON'] = '/opt/anaconda3/bin/python3.11'

    spark = SparkSession.builder \
        .appName('Recommender_system') \
        .config("spark.executor.memory", "16g") \
        .config("spark.driver.memory", "4g") \
        .config("spark.memory.offHeap.enabled", True) \
        .config("spark.memory.offHeap.size", "4g") \
        .config("spark.executor.memoryOverhead", "2g") \
        .getOrCreate()
    
    ratings_csv_path = "ratings.csv"
    ratings_df = spark.read.csv(ratings_csv_path, header=True, inferSchema=True)
    ratings_df = ratings_df.drop("timestamp")

    # ALS modelini oluşturma ve eğitme
    als = ALS(maxIter=15, regParam=0.01, rank=10, userCol="userId", itemCol="movieId", ratingCol="rating")
    als_model = als.fit(ratings_df)
 
    new_user_ratings_df = spark.createDataFrame([Row(userId=row['userId'], movieId=row['movieId'], rating=row['rating']) for row in new_user_ratings])

    # Yeni kullanıcının oylamaları ile mevcut oylamaları birleştir
    combined_ratings_df = ratings_df.union(new_user_ratings_df)

    # ALS modelini birleştirilmiş oylamalar ile yeniden eğit
    als_model = als.fit(combined_ratings_df)

    # Yeni kullanıcıya önerilerde bulunmak için kullanıcı DataFrame'i oluştur
    new_user_df = spark.createDataFrame([Row(userId=new_user_id)])

    # Kullanıcı için önerilerde bulun
    user_recommendations = als_model.recommendForUserSubset(new_user_df, 10)

    # Önerileri liste olarak almak
    recommendations_list = user_recommendations.collect()[0].recommendations
    recommended_movie_ids = [row.movieId for row in recommendations_list]

    return recommended_movie_ids


