from google.modules import standard_search
import requests
import re
import random
import time
from bs4 import BeautifulSoup
from requests.utils import unquote
from urllib.parse import urlparse
with open('movie_titles.txt', 'r') as myfile:
    movies = myfile.readlines()
j = 0
for movie in movies:
    movie = movie[movie.find(','):]
    movie = movie[1:]
    year = movie[0:movie.find(',')]
    name = movie[movie.find(','):]
    name = name[1:name.find('\n')]
    query = "%s %s"%(name,year)
    query = query.replace("'", "")
    query = query.replace("&", "and")
    print(query)
    url = "http://search.yahoo.com/search?p=%s"
    r = requests.get(url % query)
    soup = BeautifulSoup(r.text, "html.parser")
    divs = soup.findAll("div", attrs={"class": "compTitle options-toggle"})
    print(r.url)
    results = []
    for li in divs:
        a = li.find("a")
        link = a["href"]
        web_name = link[link.find('.')+1:]
        web_name = web_name[:web_name.find('.')]
        if web_name == "imdb":
            print("IMDB:")
            print(link)
            imdb = requests.get(link)
            imdb_soup = BeautifulSoup(imdb.text, "html.parser")
            j = j+1
            print(j)
            break
        elif web_name == "rottentomatoes" :
            print("Rotten Tomatoes:")
            print(link)
            imdb = requests.get(link)
            imdb_soup = BeautifulSoup(imdb.text, "html.parser")
            j = j+1
            print(j)
            break
print(j)


