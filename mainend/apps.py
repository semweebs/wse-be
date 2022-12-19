from django.apps import AppConfig
import rdflib
from rdflib.namespace import RDF

class rdf:
    def __init__(self):
        self.graph = rdflib.Graph()
    def parse_ttl(self):
        self.graph.parse("anime_csv.ttl")
    def query_rdf(self, kueri):
        return self.graph.query(kueri)

rdf_start = rdf()

def startup():
    rdf_start.parse_ttl()
    print(rdf_start)
    print(len(rdf_start.graph))

class MainendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainend'
    def ready(self):
        import os
        if os.environ.get('RUN_MAIN'):
            startup()
