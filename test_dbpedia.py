import requests

q = """
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT ?abstract WHERE {
  <http://dbpedia.org/resource/Inception> dbo:abstract ?abstract .
  FILTER(lang(?abstract) = 'en')
}
LIMIT 1
"""

r = requests.get(
    "https://dbpedia.org/sparql",
    params={"query": q},
    headers={
        "Accept": "application/sparql-results+json",
        "User-Agent": "Projekt-Webentwicklung (student)"
    },
    timeout=60
)

print(r.status_code)
print(r.text[:500])
