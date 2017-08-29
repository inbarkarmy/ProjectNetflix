from sklearn.preprocessing import OneHotEncoder
import numpy as numpy
import pandas as pd
import json
import math

#max distance between movies - define as needed
maxDist = 4

def caculateVecDistance(binaryVec1, binaryVec2 ):
    dist=maxDist
    if len(binaryVec1)==len(binaryVec2):
        for i in range(len(binaryVec1)):
            if binaryVec1[i]==binaryVec2[i]:
                if binaryVec2[i]==1:
                    dist=dist-1
    return dist

#genreWeghit = 4
#rateWeight = 2
#yearWeight = 0.01
#def TwoMoviesDist(genreVec1, rate1, year1, genreVec2, rate2, year2):
def TwoMoviesDist(genreVec1, genreVec2):

    genreDist = caculateVecDistance(genreVec1,genreVec2)
    #if rate1>rate2:
    #    rateDist = rate1-rate2
    #else:
    #    rateDist = rate2-rate1
    #if year1 > year2:
    #    yearDist = year1 - year2
    #else:
    #    yearDist = year2 - year1
    #totalDist = (genreWeghit*genreDist)+(rateWeight*rateDist)+(yearWeight*yearDist)
    #return totalDist
    return genreDist


def createMovieDistancesMatrix():
    data = pd.read_csv('Movies_info.csv', encoding='latin1')
    moviesNum =len(data["title"])
    genreMatrix = createGenreMatrix()
    res = numpy.zeros((moviesNum, moviesNum))
    i=0
    for movie1 in data["title"]:
        j=0
        for movie2 in data["title"]:
            if i==j:
                curDist=0
            else:
                curDist = TwoMoviesDist(genreMatrix[i],genreMatrix[j])
            res[i][j] = curDist
            j=j+1
        i=i+1
    return res

def createGenreMatrix():
    data = pd.read_csv('Movies_info.csv',encoding='latin1')
    totalGenres = 22
    moviesNum= len(data["title"])
    genreMatrix = numpy.zeros((moviesNum,totalGenres+1))
    movieCount =0
    dictGenre = {0: 'Comedy', 1: 'Action', 2: 'Adventure', 3: {'Animated', 'Animation'}, 4: 'Biography', 5: 'Crime',
                 6: 'Documentary', 7: 'Drama', 8: 'Family', 9: 'Fantasy', 10: 'Film-Noir', 11: 'History',
                 12: 'Horror', 13: 'Music', 14: 'Musical', 15: 'Mystery', 16: 'Romance',
                 17: {'Science Fiction', 'Sci-Fi'}, 18: {'Sports', 'Sport'}, 19: 'Thriller', 20: 'War', 21: 'Western',
                 22: 'Fitness'}

    for row in data["title"]:
        for i in range(3):
            curGenre = "genre"+str(i)
            genreA = data[curGenre][movieCount]
            genre = str(genreA).rstrip()
            for key in range(totalGenres+1):
                if len(dictGenre.get(key))==2:
                    for val in dictGenre.get(key):
                        if genre==val:
                            genreMatrix[movieCount][key]=1
                            break
                else:
                    if genre == dictGenre.get(key):
                        genreMatrix[movieCount][key] = 1
                        break
        movieCount = movieCount + 1
    return genreMatrix

#movieDistancesMatrix = createMovieDistancesMatrix()
#movieDistancesMatrix.dump("myMat.dat")
#testMat = numpy.load("myMat.dat")
#print(testMat)


def FindKNearestNeighbors(movieNum,userID):
    with open('UserFilmList.json', 'r') as fp:
        userDict = json.load(fp)
    print("finished opening")
    usr = userDict[userID]
    #todo - change k
    K = math.sqrt((len(usr)))
    kDistArr = numpy.zeros(K)
    movieArr = numpy.zeros(K)
    rateArr = numpy.zeros(K)
    print(K)
    for i in range(K):
        kDistArr[i] = maxDist+1
    for val in usr:
        curDist = TwoMoviesDist(movieNum,val)
        for j in range(K):
            if curDist< kDistArr:
                kDistArr[j] = curDist
                movieArr[j] = val
                break
    j=0
    for movieID in movieArr:
        fileName = "mv_"
        maxID=1000000
        for i in range(7):
            if movieID < maxID:
                fileName = fileName + str(0)
                maxID = maxID/10
            else:
                break
        fileName = fileName + str(movieID)
        fileName = "\training_set\training_set" + fileName
        print(fileName)
        #skipping the first row
        iterLine = open(fileName)
        next(iterLine)
        for line in iterLine:
            ratetmp = line[line.find(',') + 1:]
            rate = ratetmp[:ratetmp.find(',')]
            curID = line[ :line.find(',')]
            print("curID:")
            print(curID)
            print("rate:")
            print(rate)
            if curID == userID:
                rateArr[j] = rate
                break
        j=j+1
    sum =0
    for p in range(K):
        sum = sum + rateArr[p]
    avg = sum/K
    print(avg)
    return avg



FindKNearestNeighbors(4,1544320)
