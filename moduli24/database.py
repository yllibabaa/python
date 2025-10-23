import sqlite3

from models import Movecreate, Movie


def create_connection():
    """ create a database connection to the SQLite database """
    connection = sqlite3.connect('movies.db')
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    """ create the movies table  in the database """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tittle TEXT NOT NULL,
        description TEXT NOT NULL
    )
    ''')
    connection.commit()
    connection.close()


create_table()


def create_movie(movie: Movecreate) -> int:
    """ Adds a new movie to the database """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO movies (tittle, description) VALUES (?, ?)", (movie.tittle, movie.description))
    connection.commit()
    movie_id = cursor.lastrowid
    connection.close()
    return movie_id


def read_movie(movie_id: int) -> Movie:
    """ Retrieves a movie by its ID """
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movies ", )
    row = cursor.fetchall()
    connection.close()
    muvies = [Movie(id=row["id"], tittle=r["tittle"], description=r["description"]) for row in row]
    return muvies


def read_movies(movie_id: int):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None

    return Movie(id=row["id"], tittle=row["tittle"], description=row["description"])


def update_movie(movie_id: int, movie: MovieCreate) -> bool:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE movies set title = ? , director = ? , Where id = ? ",
                   (movie.title, movie.director, movie_id))
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated > 0


def delete_movie(movie_id: int) -> bool:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM movies Where id = ? ", (movie_id))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return deleted > 0









