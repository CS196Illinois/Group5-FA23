import tmdbsimple as tmdb
from flask import Flask, render_template, request, redirect, url_for
import json

with open('Project/genres_movies.json') as f:
    genres_movies = json.load(f).get("genres_movies")
    
with open('Project/genres_tv.json') as f:
    genres_tv = json.load(f).get("genres_tv")
    
tmdb.API_KEY = '5a8a2d7a85da710fe84e0c72953832c3'

tmdb.REQUESTS_TIMEOUT = 5 

tmdb.REQUESTS_TIMEOUT = (2, 5)
    
app = Flask(__name__)

movies = []

@app.route('/')
def index():
    return render_template('index.html', movies=movies)

@app.route('/search_movie', methods=['POST'])
def add_task():
    search = tmdb.Search()
    movies.clear()
    movie = search.movie(query=request.form.get('movie'))
    if movie:
        for s in search.results:
            if s['vote_average'] == 0.0:
                continue;
            genre_list = get_genres(s['genre_ids'])
            if (len(genre_list)) > 0:
                movies.append(s['title'] + ' -- RATING: ' + str(s['vote_average']) + ' -- GENRES: ' + str(genre_list))
    return redirect(url_for('index'))

def get_genres(genre_ids): 
    genres = []
    for id in genre_ids:
        for genre_tv_dict in genres_tv:
            if genre_tv_dict.get("id") == id:
                genres.append(genre_tv_dict.get("name"))
        for genre_movie_dict in genres_movies:
            if genre_movie_dict.get("id") == id:
                if genre_movie_dict.get("name") not in genres:
                    genres.append(genre_movie_dict.get("name"))
    return genres
    

@app.route('/show_movie', methods=['POST']) 
def movieList(): 
    movieList = movies
    return render_template('index.html', movieList=movieList)

if __name__ == '__main__':
    app.run(debug=True)
