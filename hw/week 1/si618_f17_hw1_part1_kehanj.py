import json
import sqlite3

conn = sqlite3.connect('hw1.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS movie_genre")
cur.execute("DROP TABLE IF EXISTS movies")
cur.execute("DROP TABLE IF EXISTS movie_actor")
cur.execute("CREATE TABLE movie_genre (imdb_id TEXT, genre TEXT)")
cur.execute("CREATE TABLE movies (imdb_id TEXT, title TEXT, year TEXT, rating TEXT)")
cur.execute("CREATE TABLE movie_actor (imdb_id TEXT, actor TEXT)")

movie_list = list()
with open('movie_actors_data.txt', 'r') as json_file:
	for line in json_file:
		item = json.loads(line.rstrip())
		movie_list.append({'imdb_id': item['imdb_id'],
			'title': item['title'],
			'rating': item['rating'],
			'genres': item['genres'],
			'actors': item['actors'],
			'year': item['year']})

p1 = 'INSERT INTO movie_genre VALUES (?, ?)'
p2 = 'INSERT INTO movies VALUES (?, ?, ?, ?)'
p3 = 'INSERT INTO movie_actor VALUES (?, ?)'

for item in movie_list:
	imdb_id = item['imdb_id']
	title = item['title']
	rating = item['rating']
	year = item['year']
	for genre in item['genres']:
		cur.execute(p1, (imdb_id, genre))
	cur.execute(p2, (imdb_id, title, year, rating))
	for actor in item['actors']:
		cur.execute(p3, (imdb_id, actor))

conn.commit()

# Find top 10 genres with most movies.
print("Top 10 genres:\nGenre, Movies")
p = 'SELECT genre, COUNT(*) FROM movie_genre GROUP BY genre ORDER BY COUNT(*) DESC LIMIT 10'
for Genre, Movies in cur.execute(p).fetchall():
	print(Genre + ',' + str(Movies))

# Find number of movies broken down by year in chronological order.
print("\nMovies broken down by year:\nYear, Movies")
p = 'SELECT year, COUNT(*) FROM movies GROUP BY year ORDER BY year'
for Year, Movies in cur.execute(p).fetchall():
	print(Year + ', ' + str(Movies))

# Find all Sci-Fi movies order by decreasing rating,
# then by decreasing year if ratings are the same.
print("\nSci-Fi movies:\nTitle, Year, Rating")
p = 'SELECT title, year, rating FROM movies JOIN movie_genre USING(imdb_id) ' \
	'WHERE movie_genre.genre = "Sci-Fi" ORDER BY rating DESC, year DESC'
for Title, Year, Rating in cur.execute(p).fetchall():
	print(Title + ', ' + Year + ', ' + Rating)

# Find the top 10 actors who played in most movies in and after year 2000.
# In case of ties, sort the rows by actor name.
print("\nIn and after year 2000, top 10 actors who played in most movies:\nActor, Movies")
p = 'SELECT B.actor, COUNT(*) FROM movies A JOIN movie_actor B USING(imdb_id) ' \
	'WHERE A.year >= "2000" GROUP BY B.actor ORDER BY COUNT(*) DESC, B.actor LIMIT 10'
for Actor, Movies in cur.execute(p).fetchall():
	print(Actor + ', ' + str(Movies))

# Find pairs of actors who co-stared in 3 or more movies.
print("\nPairs of actors who co-stared in 3 or more movies:\nActor A, Actor B, Co-stared Movies")
p = 'SELECT A.actor, B.actor, COUNT(*) FROM movie_actor A JOIN movie_actor B USING(imdb_id) ' \
	'WHERE A.actor < B.actor GROUP BY A.actor, B.actor HAVING COUNT(*) >= 3 ' \
	'ORDER BY COUNT(*) DESC, A.actor, B.actor'

for a, b, c in cur.execute(p).fetchall():
	print(a + ', ' + b + ', ' + str(c))

conn.close()