import os
import sqlite3

DB_FILE = "cine.db"
SCHEMA_FILE = "schema.sql"

def main():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        cur.executescript(f.read())

    con.commit()
    con.close()
    print("DB erstellt:", DB_FILE)

if __name__ == "__main__":
    main()
