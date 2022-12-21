from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from SPARQLWrapper import SPARQLWrapper, JSON

namespace = "kb"
sparql = SPARQLWrapper(
    "http://35.224.202.205:9999/blazegraph/namespace/" + namespace + "/sparql")
sparql.setReturnFormat(JSON)


@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data['title']
        res_anime_title = []
        if title != '':
            query = """
                prefix :      <http://127.0.0.1:3333/>
                prefix ex:    <http://example.org/data/>
                prefix owl:   <http://www.w3.org/2002/07/owl#>
                prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
                prefix vcard: <http://www.w3.org/2006/vcard/ns#>
                prefix x:     <http://example.org/vocab#>
                prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
                prefix bds:   <http://www.bigdata.com/rdf/search#>

                SELECT DISTINCT ?animeId ?main_picture ?animeTitle WHERE{
                    ?animeId rdf:type ex:anime;
                        x:title ?animeTitle. 
                        """
            query += '?animeTitle bds:search "*'+title+'*" .'
            query += """
                    optional{
                        ?animeId x:main_picture ?main_picture.
                    }
                }
                ORDER BY ?animeTitle
            """
            sparql.setQuery(query)
            res_anime_title = sparql.queryAndConvert()

        return JsonResponse({"status": "success", "result": res_anime_title['results']['bindings']}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)


@csrf_exempt
def detail(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        anime_id = data['animeId']
        res_anime = []
        if anime_id != '':
            query = """
                prefix :      <http://127.0.0.1:3333/>
                prefix ex:    <http://example.org/data/>
                prefix owl:   <http://www.w3.org/2002/07/owl#>
                prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
                prefix vcard: <http://www.w3.org/2006/vcard/ns#>
                prefix x:     <http://example.org/vocab#>
                prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
                prefix bds:   <http://www.bigdata.com/rdf/search#>

                SELECT DISTINCT ?title ?type ?score ?status ?episodes ?source ?members ?favorites ?episode_duration
                ?rating
                ?sfw
                ?approved
                ?start_year
                ?start_season
                ?real_start_date
                ?real_end_date
                (GROUP_CONCAT(DISTINCT ?demographics;SEPARATOR=", ") AS ?demographic) 
                (GROUP_CONCAT(DISTINCT ?themes;SEPARATOR=", ") AS ?theme) 
                (GROUP_CONCAT(DISTINCT ?studios;SEPARATOR=", ") AS ?studio) 
                (GROUP_CONCAT(DISTINCT ?producers;SEPARATOR=", ") AS ?producer) 
                (GROUP_CONCAT(DISTINCT ?licensors;SEPARATOR=", ") AS ?licensor) 
                (GROUP_CONCAT(DISTINCT ?genres;SEPARATOR=", ") AS ?genre)
                ?synopsis
                ?main_picture
                ?trailer_url
                ?title_english
                ?title_japanese
                (GROUP_CONCAT(DISTINCT ?title_synonyms;SEPARATOR=", ") AS ?title_synonym)
                WHERE {
                """
            query += anime_id
            query += ''' rdf:type ex:anime ;
                OPTIONAL {
            '''
            query += anime_id
            query += ''' x:title ?title
                } .
                OPTIONAL {
                '''
            query += anime_id
            query += ''' x:score ?score
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:type ?tipe.
                    ?tipe rdfs:label ?type.
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:status ?statuses.
                    ?statuses rdfs:label ?status.
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:episodes ?episodes
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:source ?sources.
                    ?sources rdfs:label ?source.
                } .                      
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:members ?members
                } .                      
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:favorites ?favorites
                } .                      
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:episode_duration ?episode_durations.
                    ?episode_durations rdf:value ?episode_duration.
                } .                      
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:rating ?ratings.
                    ?ratings rdf:value ?rating.
                } .                      
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:sfw ?sfw
                } .                      
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:approved ?approved
                } .                      
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:start_year ?start_years.
                    ?start_years rdf:value ?start_year.
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:start_season ?start_seasons.
                    ?start_seasons rdfs:label ?start_season.
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:real_start_date ?real_start_date
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:real_end_date ?real_end_date
                } .
                OPTIONAL {
                    {
                        select ?genre (SAMPLE(?genr) as ?genres){
                    '''
            query += anime_id
            query += ''' x:genres ?genre.
                        ?genre rdfs:label ?genr.
                        }group by ?genre
                    }
                } .
                OPTIONAL {
                    {
                        select ?theme (SAMPLE(?them) as ?themes){
                    '''
            query += anime_id
            query += ''' x:themes ?theme.
                        ?theme rdfs:label ?them.
                        }group by ?theme
                    }
                } .
                OPTIONAL {
                    {
                        select ?demographic (SAMPLE(?demographi) as ?demographics){
                    '''
            query += anime_id
            query += ''' x:demographics ?demographic.
                        ?demographic rdfs:label ?demographi.
                        }group by ?demographic
                    }
                } .
                OPTIONAL {
                    {
                        select ?studio (SAMPLE(?studi) as ?studios){
                    '''
            query += anime_id
            query += ''' x:studios ?studio.
                        ?studio rdfs:label ?studi.
                        }group by ?studio
                    }
                } .
                OPTIONAL {
                    {
                        select ?licensor (SAMPLE(?licenso) as ?licensors){
                    '''
            query += anime_id
            query += ''' x:licensors ?licensor.
                        ?licensor rdfs:label ?licenso.
                        }group by ?licensor
                    }
                } .
                OPTIONAL {
                    {
                        select ?producer (SAMPLE(?produce) as ?producers){
                    '''
            query += anime_id
            query += ''' x:producers ?producer.
                        ?producer rdfs:label ?produce.
                        }group by ?producer
                    }
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:synopsis ?synopsis
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:main_picture ?main_picture
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:trailer_url ?trailer_url
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:title_english ?title_english
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:title_japanese ?title_japanese
                } .
                OPTIONAL {
                    '''
            query += anime_id
            query += ''' x:title_synonyms ?title_synonyms
                } .
                }GROUP BY ?title ?type ?score ?status ?episodes ?source ?members ?favorites ?episode_duration
                ?rating
                ?sfw
                ?approved
                ?start_year
                ?start_season
                ?real_start_date
                ?real_end_date
                ?synopsis
                ?main_picture
                ?trailer_url
                ?title_english
                ?title_japanese
            '''
            try:
                sparql.setQuery(query)
                res_anime = sparql.queryAndConvert()
                return JsonResponse({"status": "success", "result": res_anime['results']['bindings'], }, status=200)
            except Exception as e:
                return JsonResponse({"status": "error","message":e}, status=401)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def studio(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        studio = data['studio']
        res_studio = []
        if studio != '':
            query = (f"""
                prefix :      <http://127.0.0.1:3333/>
                prefix ex:    <http://example.org/data/>
                prefix owl:   <http://www.w3.org/2002/07/owl#>
                prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
                prefix vcard: <http://www.w3.org/2006/vcard/ns#>
                prefix x:     <http://example.org/vocab#>
                prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
                prefix bds:   <http://www.bigdata.com/rdf/search#>

                SELECT DISTINCT ?studioid (SAMPLE(?studioname) AS ?studioName) WHERE{{
                    ?studioid rdf:type ex:studio ;
                                rdfs:label ?studioname.
                    ?studioname bds:search "*{studio}*"
                }}
                GROUP BY ?studioid
                ORDER BY ?studioname
            """)
            sparql.setQuery(query)
            print(query)
            res_studio = sparql.queryAndConvert()

        return JsonResponse({"status": "success", "result": res_studio['results']['bindings']}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def anime_studio(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        studio_id = data['studioId']
        res_anime = []
        if studio_id != '':
            query = (f"""
                prefix :      <http://127.0.0.1:3333/>
                prefix ex:    <http://example.org/data/>
                prefix owl:   <http://www.w3.org/2002/07/owl#>
                prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
                prefix vcard: <http://www.w3.org/2006/vcard/ns#>
                prefix x:     <http://example.org/vocab#>
                prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
                prefix bds:   <http://www.bigdata.com/rdf/search#>

                SELECT DISTINCT ?animeId ?main_picture ?animeTitle WHERE{{
                    ?animeId rdf:type ex:anime;
                        x:title ?animeTitle;
                        x:studios  {studio_id}.
                    optional{{
                        ?animeId x:main_picture ?main_picture.
                    }}
                }}
                ORDER BY ?animeTitle
            """)
            sparql.setQuery(query)
            res_anime = sparql.queryAndConvert()

        return JsonResponse({"status": "success", "result": res_anime['results']['bindings']}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)