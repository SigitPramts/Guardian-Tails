import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="paws",
    user="postgres",
    password="c00l1234",
)
