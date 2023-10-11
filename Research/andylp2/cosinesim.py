import pandas as pd 
import numpy as np
from IPython.display import display
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("c:/Users/theob/OneDrive/Desktop/Group5-FA23/Research/andylp2/tmdb_movies_data.csv").reset_index()
#for col in df.columns:
    #print(col)
#df['id']
#print(df.vote_average.to_string(index=True))

features = ['keywords', 'cast', 'genres', 'director', 'overview', 'production_companies', 'tagline']
for feature in features:
    df[feature] = df[feature].fillna('')

def combined_features(row):
    return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']+" "+row['overview']+" "+row['production_companies']+" "+row['tagline']
df["combined_features"] = df.apply(combined_features, axis =1)
df["combined_features"]

#print(" original dataframe \n", df["combined_features"])
 
# replace '_' with '-'
#df["combined_features"] = df["combined_features"].replace('|', ' ', regex=True)
 
# print dataframe
#print(" After replace character \n", df["combined_features"])

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])
#print("Count Matrix:", count_matrix.toarray())

cosine_sim = cosine_similarity(count_matrix)

#df[df['original_title'].str.contains("Super")]['original_title']
#^ testing to see if movies are in the list

movie_user_likes = "The Prestige"
if (movie_user_likes in df['original_title'].unique()) == False:
    raise Exception("movie not found")

def get_index_from_title(title):
    return df[df["original_title"] == title]["index"].values[0]
movie_index = get_index_from_title(movie_user_likes)

similar_movies = list(enumerate(cosine_sim[movie_index]))
#similar_movies

sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1], reverse=True)
#sorted_similar_movies

def get_title_from_index(index):
    return df[df.index == index]["original_title"].values[0]

i=0
for movie in sorted_similar_movies:
    print(get_title_from_index(movie[0]))
    i=i+1
    if i>15:
        break