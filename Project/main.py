import tmdbsimple as tmdb
from flask import Flask, render_template, request, redirect, url_for

tmdb.API_KEY = '5a8a2d7a85da710fe84e0c72953832c3'

tmdb.REQUESTS_TIMEOUT = 5 

tmdb.REQUESTS_TIMEOUT = (2, 5)

movie = tmdb.Movies(603)
response = movie.info()
movie.title

movie.budget

response = movie.releases()
    
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
            movies.append(s['title'])
    print(movies)
    return redirect(url_for('index'))

@app.route('/show_movie', methods=['POST']) 
def movieList(): 
    movieList = movies
    return render_template('index.html', movieList=movieList)

if __name__ == '__main__':
    app.run(debug=True)
