from google.modules import standard_search
import requests
import re
import random
import time
from requests.utils import unquote
from urllib.parse import urlparse
with open('movie_titles.txt', 'r') as myfile:
    movies = myfile.readlines()
for movie in movies:
    movie = movie[movie.find(','):]
    movie = movie[1:]
    year = movie[0:movie.find(',')]
    name = movie[movie.find(','):]
    name = name[1:]
    print(name)
    res_search = standard_search.search(name, 1)
    for s in res_search:
        link = s.link
        linkStr = urlparse(link)
        print(linkStr[1])
        linkStr = linkStr[1]
        web_name = linkStr[linkStr.find('.'):linkStr.find('.')]
        print(web_name)
        print(s.name)
        print(s.link)
    rand = random.uniform(0.1, 5)
    time.sleep(rand)


