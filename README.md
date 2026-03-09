# CineBase 

Eine Film-Datenbank-Webanwendung mit automatischer Datenerfassung aus Wikidata. Entwickelt von Gruppe 01 (webws25_01).

## Über das Projekt
CineBase ruft Filmdaten automatisch von Wikidata ab und speichert sie in einer SQLite-Datenbank. Die Webanwendung ermöglicht das Durchsuchen und Filtern von Filmen nach verschiedenen Kriterien.

## Features
- Automatische Daten-Pipeline von Wikidata
- Filterfunktionen: Titel, Genre, Nation, Erscheinungsjahr
- Detailansichten für Filme, Schauspieler, Genres und Nationen
- Responsive Design
- Datenqualitätsprüfung

## Technologien
- Backend: Python mit Bottle Framework
- Datenbank: SQLite3
- Datenabruf: SPARQL (Wikidata)
- Tools: Pandas, Jupyter Notebooks

## Installation

```bash
# Repository klonen
git clone https://code.fbi.h-da.de/we-ws-25-26/project-1.git
cd project-1

# Abhängigkeiten installieren
pip install bottle requests pandas jupyter

# Datenbank erstellen
python create_db.py

# Daten-Pipeline ausführen
python pipeline_web.py
# Oder: jupyter notebook pipeline.ipynb

# Webserver starten
python app.py

project-1/
├── app.py                 # Hauptanwendung
├── cine.db                # SQLite Datenbank
├── create_db.py           # Datenbank-Erstellung
├── pipeline_web.py        # Daten-Pipeline
├── pipeline.ipynb         # Jupyter Notebook Pipeline
├── schema.sql             # Datenbank-Schema
├── static/                # CSS, Bilder
├── views/                 # HTML-Templates
└── pipeline/export/       # Exportierte Daten (CSV, JSON)
