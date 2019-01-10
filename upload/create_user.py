import os, csv, psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]
# Create new table with user data
conn = psycopg2.connect(DATABASE_URL, sslmode="require")
curr = conn.cursor()
curr.execute("CREATE TABLE accounts (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, password VARCHAR NOT NULL);")
conn.commit()