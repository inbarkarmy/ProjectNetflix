import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def imdb_pars(imdb_soup):
        inf = imdb_soup.find("div", attrs={"class": "subtext"})
        time = inf.find("time")
        print("duration is:")
        print(time.text)
        print("genres:")
        for a in inf.findAll("a"):
            span = a.find("span", attrs={"itemprop": "genre"})
            if (span):
                print(span.text)
        inf_actors = imdb_soup.find("div", attrs={"class": "credit_summary_item"})
        print("actors:")
        for actor in inf_actors.findAll("span", attrs={"itemprop": "actors"}):
            tmp1 = actor.find("a")
            tmp2 = tmp1.find("span", attrs={"itemprop": "name"})
            print(tmp2.text)
        txtblocks = imdb_soup.findAll("div", attrs={"class": "txt-block"})
        for txtblock in txtblocks:
            fieldType = txtblock.find("h4")
            if (fieldType):
                if fieldType.text == "Country:":
                    country = txtblock.find("a")
                    if (country):
                        print(country.text)
                if fieldType.text == "Language:":
                    lang = txtblock.find("a")
                    if (lang):
                        print(lang.text)
                if fieldType.text == "Color:":
                    color = txtblock.find("a")
                    if (color):
                        print(color.text)
        recDirectorrecEllipsis = imdb_soup.find("div", attrs={"class": "rec-director rec-ellipsis"})
        if (recDirectorrecEllipsis):
            director = recDirectorrecEllipsis.text[recDirectorrecEllipsis.text.find(":") + 1:]
            print(director)
        rating = imdb_soup.find("div", attrs={"class": "ratingValue"})
        if (rating):
            print(rating.text)

def get_results(title, j):
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
        #print("web name:", web_name)
        if web_name == "imdb":
            break
            print("IMDB:", link)
            imdb = requests.get(link)
            imdb_soup = BeautifulSoup(imdb.text, "html.parser")
            imdb_pars(imdb_soup)
            j = j+1
            break
        elif web_name == "rottentomatoes":
            #print("Rotten Tomatoes:")
            #print(link)
            rotten_tomatoes = requests.get(link)
            rotten_tomatoes_soup = BeautifulSoup(rotten_tomatoes.text, "html.parser")
            print(rotten_tomatoes_soup.prettify())
            divs = rotten_tomatoes_soup.findAll("div", attrs={"class": "meta-value"})
            #print("divs:" ,divs)
            #print("genrs:", divs.find("Genres").text)
            for li in divs:
                #print("li is:", li)
                a = li.find("a")
                if a is not None:
                    print(a)
                    #genres = li.find('href')
                    #print(genres.text)
                    #kakaka = a["href"]
                    #print(kakaka)
                    #print(a.find("href"))
                    #genres = a[a.find('g')]
                    #print("this is the genres:", genres)
            j = j + 1
            break
    driver.close()
    return j

j = 0
for line in open('movie_titles.txt'):
    uid, year, title = line.split(',')
    title = title[:-1]
    search = title+' '+year
    #print(search)
    j = get_results(search, j)
    print(j)