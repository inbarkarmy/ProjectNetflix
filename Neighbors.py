from sklearn.preprocessing import OneHotEncoder
import numpy as numpy
import pandas as pd
from enum import Enum
class Build(Enum):
    nan =0
    Comedy = 1
    Documentary = 2
    Animation =3
    Family = 4
    Sports = 5
    Fitness = 6
    Crime = 7
    Drama =8
    Mystery=9
    Action = 10


data = pd.read_csv('Movies_info.csv',encoding='latin1')

#def genreToBin(totalMovies,data):
movieCount = 0
totalGenres = 22
#genreMatrix = numpy.zeroes(totalMovies,totalGenres)
genreMatrix = numpy.zeros((7,totalGenres))
movieCount =0
for row in data["name"]:
    for i in range(3):
        curGenre = "genre"+str(i)
        print(data[curGenre][movieCount])
        genre = data[curGenre][movieCount]
        if genre== 'Comedy':
            genreMatrix[movieCount][0] =1
        if genre == 'Action':
            genreMatrix[movieCount][1] =1
        if genre == 'Adventure':
            genreMatrix[movieCount][2] = 1
        if genre == 'Animation' or genre == 'Animated':
            genreMatrix[movieCount][3] = 1
        if genre == 'Biography':
            genreMatrix[movieCount][4] = 1
        if genre == 'Crime':
            genreMatrix[movieCount][5] = 1
        if genre == 'Documentary':
            genreMatrix[movieCount][6] = 1
        if genre == 'Drama':
            genreMatrix[movieCount][7] = 1
        if genre == 'Family':
            genreMatrix[movieCount][8] = 1
        if genre == 'Fantasy':
            genreMatrix[movieCount][9] = 1
        if genre == 'Film-Noir':
            genreMatrix[movieCount][10] = 1
        if genre == 'History':
            genreMatrix[movieCount][11] = 1
        if genre == 'Horror':
            genreMatrix[movieCount][12] = 1
        if genre == 'Music':
            genreMatrix[movieCount][13] = 1
        if genre == 'Musical':
            genreMatrix[movieCount][14] = 1
        if genre == 'Mystery':
            genreMatrix[movieCount][15] = 1
        if genre == 'Romance':
            genreMatrix[movieCount][16] = 1
        if genre == 'Sci-Fi' or genre =='Science Fiction':
            genreMatrix[movieCount][17] = 1
        if genre == 'Sport' or genre == 'Sports' :
            genreMatrix[movieCount][18] = 1
        if genre == 'Thriller':
            genreMatrix[movieCount][19] = 1
        if genre == 'War':
            genreMatrix[movieCount][20] = 1
        if genre == 'Western':
            genreMatrix[movieCount][21] = 1


    movieCount= movieCount+1
print(genreMatrix)