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
# for c in movie.countries:
#     if c['iso_3166_1'] == 'US':
#          print(c['certification'])

# response = search.movie(query='Marvel')
# for s in search.results:
#     print(s['title'], s['id'], s['release_date'], s['popularity'])
    
app = Flask(__name__)

# Create a list to store tasks
tasks = []

# Define a route to display the tasks
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

# Define a route to add a new task
@app.route('/search_movie', methods=['POST'])
def add_task():
    search = tmdb.Search()
    movie = search.movie(query=request.form.get('task'))
    if movie:
        for s in search.results:
            tasks.append(s['title'])
    print(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
