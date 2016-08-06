# python module
import psycopg2

# connection object
con = psycopg2.connect(database = "db", user = "postgres", password = "23051519", host = "localhost", port = "8000")

# creating a cursor for operate with data

cursor = con.cursor()

cursor.execute("INSERT INTO usuarios VALUES ('ISAIAS', 2)")

# make changes in the database
con.commit()
