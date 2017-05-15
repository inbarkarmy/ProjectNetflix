import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

def imdb_pars(imdb_soup):
        #print(imdb_soup.prettify())
        res = dict()
        inf = imdb_soup.find("div", attrs={"class": "subtext"})
        time = inf.find("time")
        Time = time.text.strip()
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
                #if fieldType.text == "Color:":
                 #   color = txtblock.find("a")
                  #  if (color):
                   #     print(color.text)
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
            res['written'] = Written
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
    title = name + ' ' + year
    print("name:", title)
    driver = webdriver.Chrome(os.path.abspath('./chromedriver_win32/chromedriver'))
    driver.get('http://www.google.com')
    elem = driver.find_element_by_id('lst-ib')
    elem.clear()
    elem.send_keys(title)
    elem.send_keys(Keys.RETURN)
    time.sleep(3)
    for elem in driver.find_elements_by_css_selector('h3.r a'):
        link = elem.get_attribute('href')
        #print(link)
        web_name = link[link.find('.') + 1:]
        web_name = web_name[:web_name.find('.')]
        if web_name == "imdb":
            imdb = requests.get(link)
            imdb_soup = BeautifulSoup(imdb.text, "html.parser")
            res = imdb_pars(imdb_soup)
            j = j+1
            break
        if web_name == "rottentomatoes":
            rotten_tomatoes = requests.get(link)
            rotten_tomatoes_soup = BeautifulSoup(rotten_tomatoes.text, "html.parser")
            res = parse_rotten_tomato(rotten_tomatoes_soup)
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
    #df = pd.DataFrame({name:[year, res['genre0'],res['genre1'],res['genre2'], res['actor0'],res['actor1'],res['actor2'], res['director'], res['time'], res['country'], res['rate']]})
    #df.to_csv(r'C:\Users\inbar\Desktop\project\ProjectNetflix\Movies_info.csv')
    #print(df)
    driver.close()
    return res

j = 0
title = []
year_ = []
duration = []
country = []
director = []
rate = []
lang = []
genre0 =[]
genre1 =[]
genre2 =[]
actor0 = []
actor1 =[]
actor2 = []
df = pd.DataFrame()
for line in open('movie_titles.txt'):
    uid, year, name = line.split(',')
    name = name[:-1]
    #print(search)
    res = get_results(name, year, j)
    title.append(name)
    year_.append(year)
    print(res['Time'])
    duration.append(res['Time'])
    country.append(res['country'])
    director.append(res['director'])
    rate.append(res['rate'])
    lang.append(res['lang'])
    genre0.append(res['genre0'])
    genre1.append(res['genre1'])
    genre2.append(res['genre2'])
    actor0.append(res['actor0'])
    actor1.append(res['actor1'])
    actor2.append(res['actor2'])
print(genre0)
df['name'] = title
df['time'] = duration
df ['director'] = director
df ['country'] = country
df ['lang'] = lang
df['rate'] = rate
df['genre0'] = genre0
df['genre1'] = genre1
df['genre2'] = genre2
df['actor0'] = actor0
df['actor1'] = actor1
df['actor2'] = actor2
df.to_csv(r'C:\Users\inbar\Desktop\project\ProjectNetflix\Movies_info.csv')
print(df)
print(j)

