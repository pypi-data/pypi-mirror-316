import heimdall

HARRY_POTTER = 'https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q216930&format=json&languages=fr|en'
tree = heimdall.getDatabase(format='api:wikidata', url=HARRY_POTTER)
heimdall.serialize(tree, format='hera:xml', url='HARRY_POTTER.xml')
