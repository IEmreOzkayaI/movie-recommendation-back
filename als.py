import os
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.ml.recommendation import ALS
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS

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


ratings_df = spark.read.csv("ratings.csv", header=True, inferSchema=True)
ratings_df = ratings_df.drop("timestamp")

# ALS modelini oluşturma ve eğitme
als = ALS(maxIter=15, regParam=0.01, rank=10, userCol="userId", itemCol="movieId", ratingCol="rating")
als_model = als.fit(ratings_df)

# Yeni kullanıcının örnek oylamaları
new_user_id = 5457
new_user_ratings = [
    Row(userId=new_user_id, movieId=1, rating=4.0),
    Row(userId=new_user_id, movieId=3, rating=3.5),
    Row(userId=new_user_id, movieId=5, rating=5.0),
    Row(userId=new_user_id, movieId=7, rating=4.5),
]

# DataFrame'e dönüştür
new_user_ratings_df = spark.createDataFrame(new_user_ratings)

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
recommendations_dict = {row.movieId: row.rating for row in recommendations_list}

# Önerileri döndür
print(recommendations_dict)
























# from pyspark.sql import SparkSession
# from pyspark.ml.recommendation import ALS


# spark = SparkSession.builder \
#     .appName('Recommender_system') \
#     .config("spark.executor.memory", "16g") \
#     .config("spark.driver.memory", "4g") \
#     .config("spark.memory.offHeap.enabled", True) \
#     .config("spark.memory.offHeap.size", "4g") \
#     .config("spark.executor.memoryOverhead", "2g") \
#     .getOrCreate()


# ratings_df = spark.read.csv("ratings.csv", header=True,inferSchema=True)
# ratings_df = ratings_df.drop("timestamp")


# train_data, test_data = ratings_df.randomSplit([0.8, 0.2], seed=123)  # biz direkt tüm veri üzerinden eğiteceğimiz için bu satıra gerek yok,performansına bakmak istersen diye silmedim
# als = ALS(maxIter=15, regParam=0.01,rank=10, userCol="userId" ,itemCol="movieId", ratingCol="rating") # extradan coldStartStrategy="drop" eklenip denenebilir.
# als_model = als.fit(ratings_df) #burada ratings_df ile database'den geleni birleştirip tüm veriyi modele verip eğiteceğiz.

# # kullanıcı için öneri yaparken de  ratings_df.filter(col("userId") == 14) gibi bir satırla ilgilendiğimiz kullanıcının verisini çekip

# # recommendations = als_model.recommendForUserSubset(new_person_ratings, numItems=10)  # burada new_person_ratings database'den çekilmiş ve spark dataframe'ine çevrilmiş yapı olacak.
# # recommendations.show(truncate=False)

# # BURADA SANA ATTIĞIM CHAT LİNKİNDEKİ önerileri liste olarak alma kısmı olacak.
# from pyspark.sql import Row

# # Yeni kullanıcının örnek oylamaları
# new_user_id = 5457
# new_user_ratings = [
#     Row(userId=new_user_id, movieId=1, rating=4.0),
#     Row(userId=new_user_id, movieId=3, rating=3.5),
#     Row(userId=new_user_id, movieId=5, rating=5.0),
#     Row(userId=new_user_id, movieId=7, rating=4.5),
# ]

# # DataFrame'e dönüştür
# new_user_ratings_df = spark.createDataFrame(new_user_ratings)

# # Yeni kullanıcının oylamaları ile mevcut oylamaları birleştir
# combined_ratings_df = ratings_df.union(new_user_ratings_df)

# # ALS modelini birleştirilmiş oylamalar ile yeniden eğit
# als_model = als.fit(combined_ratings_df)

# # Yeni kullanıcıya önerilerde bulunmak için kullanıcı DataFrame'i oluştur
# new_user_df = spark.createDataFrame([Row(userId=new_user_id)])

# # Kullanıcı için önerilerde bulun
# user_recommendations = als_model.recommendForUserSubset(new_user_df, 10)

# # Önerileri göstermek
# user_recommendations.show(truncate=False)

# # Önerileri liste olarak almak
# recommendations_list = user_recommendations.collect()[0].recommendations
# recommendations_dict = {row.movieId: row.rating for row in recommendations_list}

# # Önerileri döndür
# print(recommendations_dict)

# # Model performansını değerlendirme
# predictions_ALS = als_model.transform(test_data)
# predictions_no_missing = predictions_ALS.dropna(subset=["prediction"])

# from pyspark.ml.evaluation import RegressionEvaluator
# evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
# rmse = evaluator.evaluate(predictions_no_missing)
# print(f'Root Mean Squared Error (RMSE): {rmse}')




# """    BURASI SADECE TRAIN VE TEST'E BÖLÜNÜP MODEL EĞİTİLDİKTEN SONRA PERFORMANSINI ÖLÇME BÖLÜMÜ , PROJEDE YER ALMAYACAK.
# predictions_ALS = als_model.transform(test_data)
# # predictions_ALS.count()
# predictions_no_missing = predictions_ALS.dropna(subset=["prediction"])
# # predictions_no_missing.count()
# # prediction sonuçları için predictions_no_missing.show()

# # rmse düşük olmalı
# from pyspark.ml.evaluation import RegressionEvaluator
# evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
# rmse = evaluator.evaluate(predictions_no_missing)
# print(f'Root Mean Squared Error (RMSE): {rmse}')

# """