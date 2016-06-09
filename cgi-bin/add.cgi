#!/usr/bin/python
# Author: Brendan Sweeney

from SPARQLWrapper import SPARQLWrapper, JSON
import cgi

form = cgi.FieldStorage()
itemType = form.getvalue('type')
itemMit = form.getvalue('mit')
itemName = form.getvalue('name')
itemId = form.getvalue('id')
itemCom = form.getvalue('comment')

sparql = SPARQLWrapper("http://localhost:3030/myDataset/update")
queryString = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ghsir: <http://students.washington.edu/bps7/2014/ghsir#>

INSERT
{ GRAPH ghsir:demo
  {
  ghsir:ITEMID a ?itemType ;
    rdfs:label "ITEMNAME"@en-US ;
    rdfs:comment "ITEMCOM"@en-US ;
    ghsir:mitigates ?mitType .
  }
}
WHERE {
  { ?itemType rdfs:label "ITEMTYPE"@en-US . }
  UNION {
    GRAPH ghsir:demo {
      ?mitType rdfs:label "ITEMMIT"@en-US .
    }
  }
}
"""

queryString = queryString.replace("ITEMID",itemId)
queryString = queryString.replace("ITEMTYPE",itemType)
queryString = queryString.replace("ITEMNAME",itemName)
queryString = queryString.replace("ITEMCOM",itemCom)
queryString = queryString.replace("ITEMMIT",itemMit)
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
  print "<p>The attempted query was:</p><p>" + queryString + "</p>"

else:

  print "<h1>" + itemName + " added successfully.</h1>"

print """<a href="/index.html">Go back home</a>
</body></html>
"""
