import os
import sqlite3

from bottle import route, run, template, request, static_file, abort, error

DB_FILE = "cine.db"


def db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@route("/static/<filepath:path>")
def server_static(filepath):
    root = os.path.join(os.path.dirname(__file__), "static")
    return static_file(filepath, root=root)


@route("/")
def index():
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT id, title, year, poster_path FROM film ORDER BY id DESC LIMIT 6")
    movies = cur.fetchall()

    conn.close()
    return template("index", movies=movies)


@route("/movies")
def movies():
    q = request.query.get("q", "").strip()
    genre_id = request.query.get("genre_id", "").strip()
    nation_id = request.query.get("nation_id", "").strip()
    year_from = request.query.get("year_from", "").strip()
    year_to = request.query.get("year_to", "").strip()
    sort = request.query.get("sort", "title_asc").strip()
    
    if sort == "year_desc":
        order_by = "f.year DESC, f.title ASC"
    elif sort == "year_asc":
        order_by = "f.year ASC, f.title ASC"
    else:
        order_by = "f.title ASC"

    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM genre ORDER BY name ASC")
    all_genres = cur.fetchall()

    cur.execute("SELECT id, name FROM nation ORDER BY name ASC")
    all_nations = cur.fetchall()

    sql = """
        SELECT DISTINCT f.id, f.title, f.year, f.poster_path
        FROM film f
        LEFT JOIN film_genre fg ON fg.film_id = f.id
        WHERE 1=1
    """
    params = []

    if q:
        sql += " AND f.title LIKE ?"
        params.append(f"%{q}%")

    if genre_id.isdigit():
        sql += " AND fg.genre_id = ?"
        params.append(int(genre_id))

    if nation_id.isdigit():
        sql += " AND f.nation_id = ?"
        params.append(int(nation_id))

    if year_from.isdigit():
        sql += " AND f.year >= ?"
        params.append(int(year_from))

    if year_to.isdigit():
        sql += " AND f.year <= ?"
        params.append(int(year_to))

    sql += f" ORDER BY {order_by}"

    cur.execute(sql, params)
    movies_list = cur.fetchall()

    conn.close()

    return template(
        "movies",
        movies=movies_list,
        q=q,
        all_genres=all_genres,
        genre_id=genre_id,
        all_nations=all_nations,
        nation_id=nation_id,
        year_from=year_from,
        year_to=year_to,
        sort=sort,
    )


@route("/movie/<film_id:int>")
def movie_detail(film_id):
    conn = db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT f.*, n.name AS nation_name
        FROM film f
        LEFT JOIN nation n ON n.id = f.nation_id
        WHERE f.id = ?
        """,
        (film_id,),
    )
    film = cur.fetchone()

    if not film:
        conn.close()
        abort(404, "Film nicht gefunden")

    cur.execute(
        """
        SELECT g.id, g.name
        FROM genre g
        JOIN film_genre fg ON fg.genre_id = g.id
        WHERE fg.film_id = ?
        ORDER BY g.name ASC
        """,
        (film_id,),
    )
    genres = cur.fetchall()

    cur.execute(
        """
        SELECT p.id, p.name
        FROM person p
        JOIN film_person fp ON fp.person_id = p.id
        WHERE fp.film_id = ?
        ORDER BY p.name ASC
        """,
        (film_id,),
    )
    cast = cur.fetchall()

    conn.close()
    return template("movie_detail", film=film, genres=genres, cast=cast)


@route("/actors")
def actors():
    q = request.query.get("q", "").strip()

    conn = db()
    cur = conn.cursor()

    if q:
        cur.execute(
            "SELECT id, name FROM person WHERE name LIKE ? ORDER BY name ASC",
            (f"%{q}%",),
        )
    else:
        cur.execute("SELECT id, name FROM person ORDER BY name ASC")

    people = cur.fetchall()
    conn.close()

    return template("actors", people=people, q=q)


@route("/actor/<person_id:int>")
def actor_detail(person_id):
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM person WHERE id = ?", (person_id,))
    person = cur.fetchone()

    if not person:
        conn.close()
        abort(404, "Schauspieler nicht gefunden")

    cur.execute(
        """
        SELECT f.id, f.title, f.year
        FROM film f
        JOIN film_person fp ON fp.film_id = f.id
        WHERE fp.person_id = ?
        ORDER BY f.year DESC
        """,
        (person_id,),
    )
    films = cur.fetchall()

    conn.close()
    return template("actor_detail", person=person, films=films)


@route("/genres")
def genres():
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM genre ORDER BY name ASC")
    items = cur.fetchall()

    conn.close()
    return template("genres", genres=items)


@route("/genre/<genre_id:int>")
def genre_detail(genre_id):
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM genre WHERE id = ?", (genre_id,))
    genre = cur.fetchone()

    if not genre:
        conn.close()
        abort(404, "Genre nicht gefunden")

    cur.execute(
        """
        SELECT f.id, f.title, f.year, f.poster_path
        FROM film f
        JOIN film_genre fg ON fg.film_id = f.id
        WHERE fg.genre_id = ?
        ORDER BY f.title ASC
        """,
        (genre_id,),
    )
    movies_list = cur.fetchall()

    conn.close()
    return template("genre_detail", genre=genre, movies=movies_list)


@route("/nations")
def nations():
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM nation ORDER BY name ASC")
    items = cur.fetchall()

    conn.close()
    return template("nations", nations=items)


@route("/nation/<nation_id:int>")
def nation_detail(nation_id):
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM nation WHERE id = ?", (nation_id,))
    nation = cur.fetchone()

    if not nation:
        conn.close()
        abort(404, "Nation nicht gefunden")

    cur.execute(
        """
        SELECT id, title, year, poster_path
        FROM film
        WHERE nation_id = ?
        ORDER BY title ASC
        """,
        (nation_id,),
    )
    movies_list = cur.fetchall()

    conn.close()
    return template("nation_detail", nation=nation, movies=movies_list)


@route("/about")
def about():
    return template("about")


@route("/impressum")
def impressum():
    return template("impressum")


@route("/faq")
def faq():
    return template("faq")


@error(404)
def error404(err):
    return template("error404", err=err)


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, reloader=True)
