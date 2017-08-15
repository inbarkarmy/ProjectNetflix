from sklearn.preprocessing import OneHotEncoder
import numpy as numpy
import pandas as pd

#max distance between movies - define as needed
maxDist = 10
def caculateDistance(binaryVec1, binaryVec2 ):
    dist=maxDist
    if len(binaryVec1)==len(binaryVec2):
        for i in range(len(binaryVec1)):
            if binaryVec1[i]==binaryVec2[i]:
                if binaryVec2[i]==1:
                    dist=dist-1
    print(dist)
data = pd.read_csv('Movies_info.csv',encoding='latin1')
movieCount = 0
totalGenres = 22
genreMatrix = numpy.zeros((7,totalGenres))
movieCount =0
for row in data["name"]:
    for i in range(3):
        curGenre = "genre"+str(i)
        print(data[curGenre][movieCount])
        genre = data[curGenre][movieCount]
        dict={0:'Comedy' ,1:'Action' , 2:'Adventure' , 3:('Animated','Animation'), 4:'Biography', 5:'Crime',
              6:'Documentary', 7:'Drama',8:'Family', 9:'Fantasy', 10:'Film-Noir', 11:'History',
              12:'Horror', 13:'Music', 14:'Musical', 15:'Mystery', 16:'Romance',
              17:('Science Fiction','Sci-Fi'), 18:'Sport', 19:'Thriller', 20:'War', 21:'Western'}
        for key in range(21):
            if genre==dict.get(key):
                genreMatrix[movieCount][key]=1
    movieCount = movieCount + 1
print(genreMatrix)
#example of using caculateDistance - remove
print(caculateDistance(genreMatrix[4],genreMatrix[5]))

