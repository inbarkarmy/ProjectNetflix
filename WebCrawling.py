import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


def imdb_pars(imdb_soup):
    res = dict()
    inf = imdb_soup.find("div", attrs={"class": "subtext"})
    if inf is None:
        res['Time'] = -1
        return res
    time = inf.find("time")
    Time = ""
    if time is not None:
        Time = time.text.strip()
    if Time is None:
        res['Time'] = ""
    res['Time'] = Time
    i = 0
    for a in inf.findAll("a"):
        if i == 3:
            break
        span = a.find("span", attrs={"itemprop": "genre"})
        key = "genre" + str(i)
        if (span):
            Genre = span.text
            res[key] = Genre
            i = i + 1
    print(i)
    if i < 3:
        while i < 3:
            key = "genre" + str(i)
            res[key] = ""
            i = i + 1
    cred_sums = imdb_soup.findAll("div", attrs={"class": "credit_summary_item"})
    for cred_sum in cred_sums:
        h =  cred_sum.find("h4")
        if h.text == "Stars:":
            i = 0
            for actor in cred_sum.findAll("span", attrs={"itemprop": "actors"}):
                if i == 3:
                    break
                tmp1 = actor.find("a")
                tmp2 = tmp1.find("span", attrs={"class":"itemprop","itemprop": "name"})
                Actor = tmp2.text
                key = "actor"+str(i)
                res[key] = Actor
                i = i + 1
            if i < 3:
                while i < 3:
                    key = "actor" + str(i)
                    res[key] = ""
                    i = i + 1
    txtblocks = imdb_soup.findAll("div", attrs={"class": "txt-block"})
    for txtblock in txtblocks:
        fieldType = txtblock.find("h4")
        if (fieldType):
            if fieldType.text == "Country:":
                country = txtblock.find("a")
                if (country):
                    Country = country.text
                    res['country'] = Country
            if fieldType.text == "Language:":
                lang = txtblock.find("a")
                if (lang):
                    Lang = lang.text
                    res['lang'] = Lang
    recDirectorrecEllipsis = imdb_soup.find("div", attrs={"class": "rec-director rec-ellipsis"})
    if (recDirectorrecEllipsis):
        Director = recDirectorrecEllipsis.text[recDirectorrecEllipsis.text.find(":") + 1:]
        res['director'] = Director.strip()
    rating = imdb_soup.find("div", attrs={"class": "ratingValue"})
    if (rating):
        Rate = rating.text.strip()
        res['rate'] = Rate
    for i in res:
        print(i, res[i])
    return res

def parse_rotten_tomato(rotten_tomatoes_soup):
    res = dict()
    All = rotten_tomatoes_soup.findAll("li", attrs={"class": "meta-row clearfix"})
    for li in All:
        category = li.find("div", attrs={"class": "meta-label subtle"})
        category_n = category.text.strip()
        i = 0
        if category_n == "Genre:":
            a = li.findAll("a")
            for g in a:
                if g is not None:
                    AllGenres = g.text
                    genres = re.split('& | ,', AllGenres.strip())
                    print(genres)
                    for x in genres:
                        if i == 3:
                            break
                        key = "genre" + str(i)
                        res[key] = x
                        i = i + 1
                if i < 3:
                    while i < 3:
                        key = "genre" + str(i)
                        res[key] = ""
                        i = i + 1
        if category_n == "Runtime:":
            t = li.find("time")
            Time = t.text.strip()
            res['Time'] = Time
        if category_n == "Directed By:":
            a = li.find('a')
            Directed = a.text.strip()
            Directed = Directed[:Directed.find(',')]
            res['director'] = Directed
        if category_n == "Written By:":
            a = li.find('a')
            Written = a.text.strip()
            #res['written'] = Written
    All = rotten_tomatoes_soup.findAll("section", attrs={"class": "panel panel-rt panel-box "})
    for sec in All:
        category = sec.find("h2", attrs={"class": "panel-heading"})
        category_n = category.text.strip()
        i = 0
        if category_n == "Cast":
            AllAct = sec.findAll("a", attrs={"class": "unstyled articleLink"})
            for act in AllAct:
                if i == 3:
                    break
                key = "actor" + str(i)
                act = act.find("span")
                if act is not None:
                    Actor = act.text.strip()
                    res[key] = Actor
                i = i + 1
            if i < 3:
                while i < 3:
                    key = "genre" + str(i)
                    res[key] = ""
                    i = i + 1
    for i in res:
        print(i, res[i])
    return res

def get_results(name, year, j):
    res = dict()
    title = name + ' ' + year
    print("name:", title)
    driver = webdriver.Chrome(os.path.abspath('./chromedriver_win32/chromedriver'))
    driver.get('http://www.google.com')
    elem = driver.find_element_by_id('lst-ib')
    elem.clear()
    elem.send_keys(title)
    elem.send_keys(Keys.RETURN)
    #time.sleep(0.2)
    for elem in driver.find_elements_by_css_selector('h3.r a'):
        link = elem.get_attribute('href')
        #print(link)
        web_name = link[link.find('.') + 1:]
        web_name = web_name[:web_name.find('.')]
        if web_name == "imdb":
            if link.find("quotes") == -1 and link.find("epcast") == -1:
                imdb = requests.get(link)
                imdb_soup = BeautifulSoup(imdb.text, "html.parser")
                res = imdb_pars(imdb_soup)
                if res != -1:
                    j = j+1
                    break
        if web_name == "rottentomatoes":
            if link.find("reviews") == -1 :
                rotten_tomatoes = requests.get(link)
                rotten_tomatoes_soup = BeautifulSoup(rotten_tomatoes.text, "html.parser")
                res = parse_rotten_tomato(rotten_tomatoes_soup)
                if res != -1:
                    j = j + 1
                    break
    if 'Time' not in res.keys():
        res['Time'] = ""
    if 'lang' not in res.keys():
        res['lang'] = ""
    if 'director' not in res.keys():
        res['director'] = ""
    if 'country' not in res.keys():
        res['country'] = ""
    if 'rate' not in res.keys():
        res['rate'] = ""
    if 'actor0' not in res.keys():
        res['actor0'] = ""
    if 'actor1' not in res.keys():
        res['actor1'] = ""
    if 'actor2' not in res.keys():
        res['actor2'] = ""
    if 'genre0' not in res.keys():
        res['genre0'] = ""
    if 'genre1' not in res.keys():
        res['genre1'] = ""
    if 'genre2' not in res.keys():
        res['genre2'] = ""

    driver.close()
    return res



j = 0
FILE_NAME = 'database.csv'

TITLES_LIST = ['title','year','Time','country','director',
               'lang','rate','genre0','genre1','genre2',
              'actor0','actor1','actor2']

inv_titlesDict = dict(enumerate(TITLES_LIST))
titlesDict = {v:k for k,v in inv_titlesDict.items()}

#with open (FILE_NAME,'a') as fh:
    #fh.write(','.join(TITLES_LIST)+'\n')
csvlLine = [0]*len(TITLES_LIST)
for line in open('movie_titles.txt'):
    no_id = line[line.find(',') + 1:]
    year = no_id[:no_id.find(',')]
    name = no_id[no_id.find(',') + 1:]
    name = name[:-1]
    print("year ", year, "name: ", name)
    res = get_results(name, year, j)
    res['title'] = name
    res['year'] = year

    for key in res:
        csvlLine[titlesDict[key]] = res[key]
    csvlLine = [str(x) for x in csvlLine]
    with open(FILE_NAME, 'a') as fh:
        fh.write(','.join(csvlLine) + '\n')

print(j)
