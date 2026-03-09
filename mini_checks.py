import sqlite3

DB_FILE = "cine.db"

def main():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute("PRAGMA integrity_check;")
    print("Integrity:", cur.fetchone()[0])

    cur.execute("SELECT COUNT(*) FROM film;")
    print("Filme:", cur.fetchone()[0])

    cur.execute("SELECT COUNT(*) FROM person;")
    print("Personen:", cur.fetchone()[0])

    cur.execute("SELECT COUNT(*) FROM genre;")
    print("Genres:", cur.fetchone()[0])

    cur.execute("SELECT COUNT(*) FROM nation;")
    print("Nationen:", cur.fetchone()[0])

    cur.execute("""
        SELECT title, COUNT(*) c
        FROM film
        GROUP BY title
        HAVING c > 1;
    """)
    print("Doppelte Filmtitel:", cur.fetchall())

    cur.execute("SELECT COUNT(*) FROM film WHERE description IS NULL OR TRIM(description) = '';")
    print("Filme ohne Beschreibung:", cur.fetchone()[0])

    con.close()

if __name__ == "__main__":
    main()
