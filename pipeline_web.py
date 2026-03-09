# Pipeline: füllt cine.db aus Webdaten (Wikidata
import sqlite3
import time
import requests
DB_FILE = "cine.db"
ENDPOINT = "https://query.wikidata.org/sparql"
UA = "Projekt-Webentwicklung (student)"

MOVIES = [
    ("Inception", 2010),
    ("The Dark Knight", 2008),
    ("Fight Club", 1999),
    ("Pulp Fiction", 1994),
    ("The Matrix", 1999),
    ("Interstellar", 2014),
    ("Titanic", 1997),
    ("Alien", 1979),
    ("Trainspotting", 1996),
]

def sparql(query):
    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": UA
    }
    for _ in range(3):
        try:
            r = requests.get(ENDPOINT, params={"query": query}, headers=headers, timeout=60)
            if r.status_code == 429:
                time.sleep(5)
                continue
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException:
            time.sleep(2)
    return None

def one_row(cur, sql, params=()):
    cur.execute(sql, params)
    return cur.fetchone()

def get_or_create(cur, table, name, wikidata_uri=None):
    row = one_row(cur, f"SELECT id FROM {table} WHERE name = ?", (name,))
    if row:
        return row[0]

    cur.execute(
        f"INSERT INTO {table} (name, wikidata_uri, dbpedia_uri) VALUES (?, ?, ?)",
        (name, wikidata_uri, None)
    )
    return cur.lastrowid

def get_film_id(cur, title, year):
    row = one_row(cur, "SELECT id FROM film WHERE title = ? AND year = ? LIMIT 1", (title, year))
    return row[0] if row else None

def upsert_film(cur, title, year, description, poster_path, film_wd_uri, nation_id):
    film_id = get_film_id(cur, title, year)
    if film_id is None:
        cur.execute(
            """INSERT INTO film (title, year, description, poster_path, wikidata_uri, dbpedia_uri, nation_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (title, year, description, poster_path, film_wd_uri, None, nation_id)
        )
        return cur.lastrowid
    else:
        cur.execute(
            """UPDATE film
               SET description = ?, poster_path = ?, wikidata_uri = ?, nation_id = ?
               WHERE id = ?""",
            (description, poster_path, film_wd_uri, nation_id, film_id)
        )
        return film_id

def find_film_on_wikidata(title, year):
    # Suche Film über englisches Label + Jahr
    t = title.replace('"', '\\"')
    q = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?film WHERE {{
      ?film wdt:P31/wdt:P279* wd:Q11424 .
      ?film rdfs:label ?lab .
      FILTER(LANG(?lab) = "en")
      FILTER(LCASE(STR(?lab)) = LCASE("{t}"))
      ?film wdt:P577 ?date .
      BIND(YEAR(?date) AS ?y)
      FILTER(?y = {year})
    }}
    LIMIT 1
    """
    data = sparql(q)
    rows = data["results"]["bindings"] if data else []
    return rows[0]["film"]["value"] if rows else None

def get_description(film_wd_uri, lang):
    q = f"""
    PREFIX schema: <http://schema.org/>

    SELECT ?d WHERE {{
      <{film_wd_uri}> schema:description ?d .
      FILTER(lang(?d) = "{lang}")
    }}
    LIMIT 1
    """
    data = sparql(q)
    rows = data["results"]["bindings"] if data else []
    return rows[0]["d"]["value"] if rows else ""

def get_details(film_wd_uri):
    # Nation, Genre, Cast (Labels)
    q = f"""
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    PREFIX wikibase: <http://wikiba.se/ontology#>

    SELECT ?country ?countryLabel ?genre ?genreLabel ?cast ?castLabel WHERE {{
      OPTIONAL {{ <{film_wd_uri}> wdt:P495 ?country . }}
      OPTIONAL {{ <{film_wd_uri}> wdt:P136 ?genre . }}
      OPTIONAL {{ <{film_wd_uri}> wdt:P161 ?cast . }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 80
    """
    data = sparql(q)
    return data["results"]["bindings"] if data else []

def pick_poster(i):
    n = (i % 5) + 1
    return f"posters/poster{n}.jpg"

def main():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    for i, (title, year) in enumerate(MOVIES):
        print("Hole:", title, year)

        film_uri = find_film_on_wikidata(title, year)
        if not film_uri:
            print("  WARN: nichts gefunden")
            continue

        desc = get_description(film_uri, "de")
        if not desc:
            desc = get_description(film_uri, "en")

        rows = get_details(film_uri)

        nation_id = None
        genres = set()
        cast = []

        for r in rows:
            if nation_id is None and "countryLabel" in r:
                nation_name = r["countryLabel"]["value"]
                nation_uri = r["country"]["value"] if "country" in r else None
                nation_id = get_or_create(cur, "nation", nation_name, nation_uri)

            if "genreLabel" in r:
                gname = r["genreLabel"]["value"]
                guri = r["genre"]["value"] if "genre" in r else None
                gid = get_or_create(cur, "genre", gname, guri)
                genres.add(gid)

            if "castLabel" in r and len(cast) < 6:
                cast.append(r["castLabel"]["value"])

        poster_path = pick_poster(i)
        film_id = upsert_film(cur, title, year, desc, poster_path, film_uri, nation_id)

        # Links neu setzen (einfach + übersichtlich)
        cur.execute("DELETE FROM film_genre WHERE film_id = ?", (film_id,))
        cur.execute("DELETE FROM film_person WHERE film_id = ?", (film_id,))

        for gid in genres:
            cur.execute(
                "INSERT OR IGNORE INTO film_genre (film_id, genre_id) VALUES (?, ?)",
                (film_id, gid)
            )

        for name in cast:
            pid = get_or_create(cur, "person", name)
            cur.execute(
                "INSERT OR IGNORE INTO film_person (film_id, person_id, role) VALUES (?, ?, ?)",
                (film_id, pid, "Cast")
            )

        con.commit()
        print("  OK, Beschreibung Länge:", len(desc))
        time.sleep(1)

    con.close()
    print("Fertig: Daten in cine.db gespeichert.")

if __name__ == "__main__":
    main()
