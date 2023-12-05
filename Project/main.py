import tmdbsimple as tmdb
from flask import Flask, render_template, request, redirect, url_for
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

with open('Project/genres_movies.json') as f:
    genres_movies = json.load(f).get("genres_movies")
    
with open('Project/genres_tv.json') as f:
    genres_tv = json.load(f).get("genres_tv")
    
tmdb.API_KEY = '5a8a2d7a85da710fe84e0c72953832c3'

tmdb.REQUESTS_TIMEOUT = 5 

tmdb.REQUESTS_TIMEOUT = (2, 5)
    
app = Flask(__name__)

movies = []

sorted_by_popularity = []

df = pd.read_csv("Project/tmdb_movies_data.csv").reset_index()

features = ['keywords', 'cast', 'genres', 'director', 'overview', 'production_companies', 'tagline']
for feature in features:
    df[feature] = df[feature].fillna('')

def combined_features(row):
    return row['keywords'].replace('|', " ")+" "+row['cast'].replace('|', " ")+" "+row['genres'].replace('|', " ")+row['genres'].replace('|', " ")+" "+row['director']+" "+row['overview']+" "+row['production_companies'].replace('|', " ")+" "+row['tagline']
df["combined_features"] = df.apply(combined_features, axis =1)

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])
#print("Count Matrix:", count_matrix.toarray())

cosine_sim = cosine_similarity(count_matrix)

@app.route('/')
def index():
    """
    Renders the index.html template with the movies list.
    """
    return render_template('index.html', sorted_by_popularity=sorted_by_popularity)

@app.route('/search_movie', methods=['POST'])
def add_task():
    """
    Searches for movies based on the user's input and adds them to the movies list.
    """
    search = tmdb.Search()
    search.movie(query=request.form.get('movie'))
    movie = (search.results[0]['original_title'])
    if (movie in df['original_title'].unique()) == False:
        return redirect(url_for('index'))
        
    index = df[df["original_title"] == movie]["index"].values[0]
    
    similar_movies = list(enumerate(cosine_sim[index]))
    
    sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1], reverse=True)

    sorted_by_popularity.clear()
    
    i = 0
    
    for movie in sorted_similar_movies:
        #print(get_title_from_index(movie[0]))
        #print(sorted_similar_movies[i])
        sorted_by_popularity.append(df[df.index == movie[0]]["original_title"].values[0])
        #print(df[df.original_title == "Jurassic World"]["popularity"])
        i+=1
        if i>10:
            break
        
        
    print(sorted_by_popularity)
        
    # if movie:
    #     for s in search.results:
    #         if s['vote_average'] > 0.0:
    #             genre_list = get_genres(s['genre_ids'])
    #             if (len(genre_list)) > 0:
    #                 movies.append(f"{s['title']} -- RATING: {str(s['vote_average'])} -- GENRES: {str(genre_list)}")
    return redirect(url_for('index'))

@app.route('/show_movie', methods=['POST']) 
def movieList(): 
    """
    Renders the index.html template with the movieList.
    """
    print("SDRTYUIOOLIUYTRDFGHJKL:OIUYTRDFGHJKIUYTRDFGHJKIOIUYTRFDFGHJKLOIUYTRFDFGHJ\n\n\n\n\n\n")
    print(type(sorted_by_popularity))

    return render_template('index.html', sorted_by_popularity=sorted_by_popularity)

if __name__ == '__main__':
    app.run()
