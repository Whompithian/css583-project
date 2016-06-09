#!/usr/bin/python
# Author: Brendan Sweeney

from SPARQLWrapper import SPARQLWrapper, JSON
import cgi

sparql = SPARQLWrapper("http://localhost:3030/myDataset/query")
queryString = """
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?title WHERE {

  ?class a rdfs:Class ;
    rdfs:label ?title .
}
ORDER BY ?title
"""

sparql.setQuery(queryString)

sparql.setReturnFormat(JSON)

try:
  results = sparql.query().convert()
  requestGood = True
except Exception, e:
  results = str(e)
  requestGood = False

if requestGood:
  queryString = """
  PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX ghsir: <http://students.washington.edu/bps7/2014/ghsir#>

  SELECT ?title WHERE {
    GRAPH ghsir:demo {
      ?class a ghsir:Vulnerability ;
        rdfs:label ?title .
    }
  }
  ORDER BY ?title
  """

  sparql.setQuery(queryString)

  sparql.setReturnFormat(JSON)

  try:
    vulns = sparql.query().convert()
    requestGood = True
  except Exception, e:
    results = str(e)
    requestGood = False

print """Content-type: text/html

<!DOCTYPE html>
<html><head><title>Results</title>
<style type="text/css"> * { font-family: arial,helvetica}</style>
</head><body>
"""

if requestGood == False:
  print "<h1>Problem communicating with the server</h1>"
  print "<p>" + results + "</p>"
elif (len(results["results"]["bindings"]) == 0):
  print "<p>No results found.</p>"

else:

  print """<h1>Add a New Item</h1>
  <form action="/cgi-bin/add.cgi" method="get">
  <p>New Item Type: <select name="type">"""

  for result in results["results"]["bindings"]:
    selection = result["title"]["value"]
    print '<option value="' + selection + '">' + selection + '</option>'

  print '</select><p>Mitigates: <select name="mit">'

  for result in vulns["results"]["bindings"]:
    selection = result["title"]["value"]
    print '<option value="' + selection + '">' + selection + '</option>'

  print """</select></p>
  <p>Name: <input type="text" name="name"/></p>
  <p>Unique ID: <input type="text" name="id"/></p>
  <p>Comment: <input type="text" name="comment"/></p>
  <input type="submit" value="Submit"/>
  </form>"""

print """<a href="/index.html">Go back home</a>
</body></html>
"""
