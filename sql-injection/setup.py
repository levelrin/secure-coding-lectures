import psycopg2

connection = psycopg2.connect(
    host="sql-injection-sql-injection-db-1",
    database="sql-injection",
    user="postgres",
    password="postgres"
)

cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE users (
        id    TEXT  PRIMARY KEY,
        name  TEXT  NOT NULL
    );
    """
)
connection.commit()

cursor.close()
connection.close()
