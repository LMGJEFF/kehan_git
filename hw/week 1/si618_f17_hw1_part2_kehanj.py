import sqlite3
import sys

genre = sys.argv[1]
k = sys.argv[2]

conn = sqlite3.connect('hw1.db')
cur = conn.cursor()

p = 'SELECT A.actor, COUNT(*) FROM movie_actor A JOIN movie_genre B USING(imdb_id) ' + \
	'WHERE B.genre = "' + genre + '" GROUP BY A.actor ORDER BY COUNT(*) DESC, A.actor LIMIT ' + k	

print("Top " + k + " actors who played in most " + genre + " movies:")
print("Actor, " + genre + " Movies Played in")

for a, b in cur.execute(p).fetchall():
	print(a + ', ' + str(b))

conn.close()