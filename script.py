import sqlite3
import csv
 
conn = sqlite3.connect('output.sqlite')
 
cur = conn.cursor()
 
cur.execute("CREATE TABLE movies(movieId,title,genres)")
 
reader = csv.reader(open('ml-25m/movies.csv', "rb",encoding=ascii))
for row in reader:
    to_db = [(row[0], "utf8"), (row[1], "utf8"), row[2], row[3]]
    cur.execute("INSERT INTO lookup (movieId,title,genres) VALUES (?, ?, ?, ?);", to_db)
    #cur.execute("CREATE INDEX location_idx ON lookup(location)" )
conn.commit()