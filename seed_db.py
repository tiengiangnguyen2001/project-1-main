import sqlite3

DB_FILE = "cine.db"

def get_or_create(cur, table, name):
    cur.execute(f"SELECT id FROM {table} WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
    return cur.lastrowid

def main():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    usa = get_or_create(cur, "nation", "USA")
    thriller = get_or_create(cur, "genre", "Thriller")
    scifi = get_or_create(cur, "genre", "Sci-Fi")
    leo = get_or_create(cur, "person", "Leonardo DiCaprio")

    cur.execute(
        "INSERT INTO film (title, year, description, poster_path, nation_id) VALUES (?, ?, ?, ?, ?)",
        ("Inception", 2010, "Testdatensatz (Seed).", "posters/poster1.jpg", usa)
    )
    film_id = cur.lastrowid

    cur.execute("INSERT OR IGNORE INTO film_genre (film_id, genre_id) VALUES (?, ?)", (film_id, thriller))
    cur.execute("INSERT OR IGNORE INTO film_genre (film_id, genre_id) VALUES (?, ?)", (film_id, scifi))
    cur.execute("INSERT OR IGNORE INTO film_person (film_id, person_id, role) VALUES (?, ?, ?)", (film_id, leo, "Cast"))

    con.commit()
    con.close()
    print("Seed-Testdaten eingefügt.")

if __name__ == "__main__":
    main()
