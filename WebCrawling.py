import urllib.request
from lxml.html import HTMLParser
from lxml import etree
from io import StringIO, BytesIO

IMDB_url = "http://www.imdb.com"

with urllib.request.urlopen(IMDB_url) as url:
    broken_html = url.read()
parser = etree.HTMLParser()
tree = etree.parse(StringIO(broken_html), parser)
s = tree.getroot()
print(s)
result = etree.tostring(tree.getroot(),pretty_print=True, method="html")
print(result)