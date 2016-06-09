#!/usr/bin/python
# Author: Brendan Sweeney

from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:3030/myDataset/query")
queryString = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ghsir: <http://students.washington.edu/bps7/2014/ghsir#>

SELECT DISTINCT ?vuln ?control
WHERE {
  GRAPH ghsir:demo {
    ?vulnId  a ghsir:Vulnerability ;
             rdfs:label ?vuln .
    OPTIONAL {
      ?controlId ghsir:mitigates ?vulnId ;
                 rdfs:label ?control .
    }
  }
}
"""

sparql.setQuery(queryString)

sparql.setReturnFormat(JSON)

try:
  results = sparql.query().convert()
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

  print """<h1>Known vulnerabilities and their controls</h1>
  <table border="1">
  <tr><td><b>Vulnerability</b></td>
  <td><b>Mitigating Control</b></td></td>
  </tr>
  """

  for result in results["results"]["bindings"]:
    vuln = result["vuln"]["value"]
    try:
      control = result["control"]["value"]
    except Exception, e:
      control = " "
    print "<tr><td>" + vuln + "</td><td>" + control + "</td></tr>"

  print "</table>"

print """<a href="/index.html">Go back home</a>
</body></html>
"""
