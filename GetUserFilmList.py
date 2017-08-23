import glob
import os


def CreateUsersFilmsDictionary():

    # parameters:
    i =0
    j=0
    curr_path = os.path.dirname(os.path.abspath(__file__))
    path = curr_path + r'\training_set\training_set\*.txt'
    UserFilmDictionary = dict()

    #create a lint of all files
    files = glob.glob(path)
    # iterate over the list getting each file

    for fle in files:
        i = i+1
        print(i)
        #open the file and then call .read() to get the text
        for line in open(fle):
            j = j + 1
            if j == 1:
                continue
            user = line[:line.find(',')]
            if user not in UserFilmDictionary:
                UserFilmDictionary.setdefault(user, [])
            UserFilmDictionary[user].append(i)
    for user in UserFilmDictionary:
        print ("films that user ", user," rated:")
        for film in UserFilmDictionary[user]:
            print(film)



