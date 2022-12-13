from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import mainend.apps

rdf = mainend.apps.rdf_start

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

                SELECT DISTINCT ?animeTitle WHERE{
                    ?animeId rdf:type ex:anime;
                        x:title ?animeTitle. 
                        """
            query += 'filter contains( lcase(?animeTitle), "'+title+'") .'
            query += """
                }
                ORDER BY ?animeTitle
            """
            res = rdf.query_rdf(query)
            for row in res:
                res_anime_title.append(row.animeTitle)
            
        return JsonResponse({"status": "success", "result":res_anime_title}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)