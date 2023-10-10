import pandas as pd 
import numpy as np
from IPython.display import display
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("c:/Users/theob/OneDrive/Desktop/Group5-FA23/Research/andylp2/movie_dataset.csv")
features = ['keywords', 'cast', 'genres', 'director']
for feature in features:
    df[feature] = df[feature].fillna('')
def combined_features(row):
    return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']
df["combined_features"] = df.apply(combined_features, axis =1)

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])
#print("Count Matrix:", count_matrix.toarray())

cosine_sim = cosine_similarity(count_matrix)

movie_user_likes = "Spirited Away"
def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]
movie_index = get_index_from_title(movie_user_likes)

similar_movies = list(enumerate(cosine_sim[movie_index]))

sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1], reverse=True)

def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]
i=0
for movie in sorted_similar_movies:
    print(get_title_from_index(movie[0]))
    i=i+1
    if i>15:
        break