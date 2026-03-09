DROP TABLE IF EXISTS film_genre;
DROP TABLE IF EXISTS film_person;
DROP TABLE IF EXISTS film;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS nation;

CREATE TABLE nation (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  wikidata_uri TEXT,
  dbpedia_uri TEXT
);

CREATE TABLE film (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  year INTEGER,
  description TEXT,
  poster_path TEXT,
  wikidata_uri TEXT,
  dbpedia_uri TEXT,
  nation_id INTEGER,
  FOREIGN KEY (nation_id) REFERENCES nation(id)
);

CREATE TABLE person (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  wikidata_uri TEXT,
  dbpedia_uri TEXT
);

CREATE TABLE genre (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  wikidata_uri TEXT,
  dbpedia_uri TEXT
);

CREATE TABLE film_person (
  film_id INTEGER NOT NULL,
  person_id INTEGER NOT NULL,
  role TEXT,
  PRIMARY KEY (film_id, person_id),
  FOREIGN KEY (film_id) REFERENCES film(id),
  FOREIGN KEY (person_id) REFERENCES person(id)
);

CREATE TABLE film_genre (
  film_id INTEGER NOT NULL,
  genre_id INTEGER NOT NULL,
  PRIMARY KEY (film_id, genre_id),
  FOREIGN KEY (film_id) REFERENCES film(id),
  FOREIGN KEY (genre_id) REFERENCES genre(id)
);
