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
                    ?ratings rdfs:label ?rating.
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
            sparql.setQuery(query)
            res_anime = sparql.queryAndConvert()
            res_character = []
            id = anime_id.split(":")
            query = (f"""
                        prefix wd: <http://www.wikidata.org/entity/>
                        prefix wds: <http://www.wikidata.org/entity/statement/>
                        prefix wdv: <http://www.wikidata.org/value/>
                        prefix wdt: <http://www.wikidata.org/prop/direct/>
                        prefix wikibase: <http://wikiba.se/ontology#>
                        prefix p: <http://www.wikidata.org/prop/>
                        prefix ps: <http://www.wikidata.org/prop/statement/>
                        prefix pq: <http://www.wikidata.org/prop/qualifier/>
                        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        prefix bd: <http://www.bigdata.com/rdf#>
                        SELECT DISTINCT * WHERE {{
                            SERVICE <https://query.wikidata.org/sparql> {{
                                SELECT ?charactersLabel (GROUP_CONCAT(?actorLabel;SEPARATOR=", ") AS ?actorsLabel) ?genderLabel WHERE {{
                                    {{
                                    SELECT DISTINCT ?charactersLabel ?actorLabel ?genderLabel WHERE {{
                                        SERVICE wikibase:label {{ 
                                            bd:serviceParam wikibase:language "en". }}
                                            {{
                                            SELECT DISTINCT ?item WHERE {{
                                                ?item p:P4086 ?statement0.
                                                ?statement0 ps:P4086 "{id[1]}".
                                            }}
                                            LIMIT 100
                                        }}
                                        OPTIONAL 
                                        {{ 
                                            ?item wdt:P674 ?characters. 
                                            ?characters wdt:P725 ?actor.
                                            ?characters wdt:P21 ?gender.
                                        }}
                                    }}
                                    }}
                                }}GROUP BY ?charactersLabel ?genderLabel
                            }}
                        }}
                        """)
            sparql.setQuery(query)
            res_character = sparql.queryAndConvert()
        return JsonResponse({"status": "success", "result": res_anime['results']['bindings'], "character": res_character['results']['bindings']}, status=200)
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

@csrf_exempt
def advance_search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        genre = data['genre']
        themes = data['themes']
        demo = data['demo']
        tipe = data['type']
        score = data['score']
        start_year = data['start_year']
        start_season = data['start_season']
        status = data['status']
        sorting_score = data['sort_score']
        res_anime = []
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
                ?animeId rdf:type ex:anime"""
        if len(genre)!=0:
            query +=(f''';
                   x:genres  ''')
            counter = 0
            for x in genre:
                counter+=1
                if(counter == len(genre)):
                    query+=(f'''ex:{x}''')
                else:
                    query+=(f'''ex:{x}, ''')
        if len(themes)!=0:
            query +=(f''';
                    x:themes  ''')
            counter = 0
            for x in themes:
                counter+=1
                if(counter == len(themes)):
                    query+=(f'''ex:{x}''')
                else:
                    query+=(f'''ex:{x}, ''')
        if len(demo)!=0:
            query +=(f''';
                    x:demographics  ''')
            counter = 0
            for x in demo:
                counter+=1
                if(counter == len(demo)):
                    query+=(f'''ex:{x}''')
                else:
                    query+=(f'''ex:{x}, ''')
        if (tipe!=''):
            query +=(f''';
                    x:type ex:{tipe}''')
        if (start_year!=''):
            query +=(f''';
                    x:start_year ex:{start_year}.0''')
        if (status!=''):
            query +=(f''';
                    x:status ex:{status} ''')
        if (start_season!=''):
            query +=(f''';
                    x:start_season ex:{start_season}''')
        query +=''';
                    x:score ?score'''
        query+=''';
                    x:title ?animeTitle.
                optional{
                    ?animeId x:main_picture ?main_picture.
                }
        '''
        if(score!=''):
            query+=(f'''
                filter (?score >= "{score}"^^xsd:double)
            ''')
        if(sorting_score == 'asc'):
            query+=('''
                }order by ?score
            '''
            )
        elif(sorting_score == 'desc'):
            query+=('''
                }order by desc (?score)
            '''
            )
        else:
            query+='''
            }
            '''
        print(query)
        sparql.setQuery(query)
        res_anime = sparql.queryAndConvert()
        print(res_anime)
        return JsonResponse({"status": "success", "result": res_anime['results']['bindings']}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def advance_data(request):
    if request.method == 'GET':
        genre =[]
        query = ("""
            prefix :      <http://127.0.0.1:3333/>
            prefix ex:    <http://example.org/data/>
            prefix owl:   <http://www.w3.org/2002/07/owl#>
            prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
            prefix vcard: <http://www.w3.org/2006/vcard/ns#>
            prefix x:     <http://example.org/vocab#>
            prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
            prefix bds:   <http://www.bigdata.com/rdf/search#>

            SELECT DISTINCT ?genreId (SAMPLE(?genreLabel) AS ?genreName) WHERE{{
                ?genreId rdf:type ex:genre;
                        rdfs:label ?genreLabel.
            }}group by ?genreId
        """)
        sparql.setQuery(query)
        genre = sparql.queryAndConvert()

        theme = []
        query = ("""
            prefix :      <http://127.0.0.1:3333/>
            prefix ex:    <http://example.org/data/>
            prefix owl:   <http://www.w3.org/2002/07/owl#>
            prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
            prefix vcard: <http://www.w3.org/2006/vcard/ns#>
            prefix x:     <http://example.org/vocab#>
            prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
            prefix bds:   <http://www.bigdata.com/rdf/search#>

            SELECT DISTINCT ?themeId (SAMPLE(?themeLabel) AS ?themeName) WHERE{{
                ?themeId rdf:type ex:theme;
                        rdfs:label ?themeLabel.
            }}group by ?themeId
        """)
        sparql.setQuery(query)
        theme = sparql.queryAndConvert()

        demo = []
        query = ("""
            prefix :      <http://127.0.0.1:3333/>
            prefix ex:    <http://example.org/data/>
            prefix owl:   <http://www.w3.org/2002/07/owl#>
            prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
            prefix vcard: <http://www.w3.org/2006/vcard/ns#>
            prefix x:     <http://example.org/vocab#>
            prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
            prefix bds:   <http://www.bigdata.com/rdf/search#>

            SELECT DISTINCT ?demographicId (SAMPLE(?demographicLabel) AS ?demographicName) WHERE{{
                ?demographicId rdf:type ex:demographic;
                        rdfs:label ?demographicLabel.
            }}group by ?demographicId
        """)
        sparql.setQuery(query)
        demo = sparql.queryAndConvert()

        tipe = []
        query = ("""
            prefix :      <http://127.0.0.1:3333/>
            prefix ex:    <http://example.org/data/>
            prefix owl:   <http://www.w3.org/2002/07/owl#>
            prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
            prefix vcard: <http://www.w3.org/2006/vcard/ns#>
            prefix x:     <http://example.org/vocab#>
            prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
            prefix bds:   <http://www.bigdata.com/rdf/search#>

            SELECT DISTINCT ?typeId (SAMPLE(?typeLabel) AS ?typeName) WHERE{{
                ?typeId rdf:type ex:tipe;
                        rdfs:label ?typeLabel.
            }}group by ?typeId
        """)
        sparql.setQuery(query)
        tipe = sparql.queryAndConvert()

        start_year = []
        query = ("""
            prefix :      <http://127.0.0.1:3333/>
            prefix ex:    <http://example.org/data/>
            prefix owl:   <http://www.w3.org/2002/07/owl#>
            prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
            prefix vcard: <http://www.w3.org/2006/vcard/ns#>
            prefix x:     <http://example.org/vocab#>
            prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
            prefix bds:   <http://www.bigdata.com/rdf/search#>

            SELECT DISTINCT ?start_yearId (SAMPLE(?start_yearLabel) AS ?start_yearName) WHERE{{
                ?start_yearId rdf:type ex:start_year;
                        rdf:value ?start_yearLabel.
            }}group by ?start_yearId
        """)
        sparql.setQuery(query)
        start_year = sparql.queryAndConvert()

        start_season = []
        query = ("""
            prefix :      <http://127.0.0.1:3333/>
            prefix ex:    <http://example.org/data/>
            prefix owl:   <http://www.w3.org/2002/07/owl#>
            prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
            prefix vcard: <http://www.w3.org/2006/vcard/ns#>
            prefix x:     <http://example.org/vocab#>
            prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
            prefix bds:   <http://www.bigdata.com/rdf/search#>

            SELECT DISTINCT ?start_seasonId (SAMPLE(?start_seasonLabel) AS ?start_seasonName) WHERE{{
                ?start_seasonId rdf:type ex:start_season;
                        rdfs:label ?start_seasonLabel.
            }}group by ?start_seasonId
        """)
        sparql.setQuery(query)
        start_season = sparql.queryAndConvert()

        status = []
        query = ("""
            prefix :      <http://127.0.0.1:3333/>
            prefix ex:    <http://example.org/data/>
            prefix owl:   <http://www.w3.org/2002/07/owl#>
            prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
            prefix vcard: <http://www.w3.org/2006/vcard/ns#>
            prefix x:     <http://example.org/vocab#>
            prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
            prefix bds:   <http://www.bigdata.com/rdf/search#>

            SELECT DISTINCT ?statusId (SAMPLE(?statusLabel) AS ?statusName) WHERE{{
                ?statusId rdf:type ex:status;
                        rdfs:label ?statusLabel.
            }}group by ?statusId
        """)
        sparql.setQuery(query)
        status = sparql.queryAndConvert()
        return JsonResponse({"status": "success", "genre": genre['results']['bindings']
                            ,"theme": theme['results']['bindings']
                            ,"demo": demo['results']['bindings']
                            ,"tipe": tipe['results']['bindings']
                            ,"start_year": start_year['results']['bindings']
                            ,"start_season": start_season['results']['bindings']
                            ,"status": status['results']['bindings']
                            }, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)