import pandas as pd
import numpy as np
import os
import codecs

def getPath():
    return "/home/vasudhaika/Desktop/classifiednews"

def getFolders():
    return os.listdir(getPath())

def joinPath(path1, path2):
    return str(path1) + "/" + str(path2)

def getfilename(foldername, articlenum):
    f = joinPath(getPath(), foldername)
    f = joinPath(f, articlenum)
    f += '.txt'
    return f

def getRow(foldername, articlenum, category):
    columns = ['Category', 'Text']

    f = codecs.open(getfilename(foldername, articlenum), 'r', 'utf-8')

    text = f.read().replace('\n', ' ')

    dic = {'Category':category, 'Text':text}

    return pd.DataFrame(dic, columns=columns, index=[0])

def main():
    listfolders = getFolders()
    print listfolders
    #columns = ['Category', 'Text']
    mydataframe =  pd.DataFrame()
    for folder in listfolders:
        articlenum = 0
        print("*****Folder "+folder+" started")
        while(os.path.isfile(getfilename(folder, articlenum))):
            category = folder.replace("_farms", '')
            mydataframe = mydataframe.append(getRow(folder, articlenum, category), ignore_index=True)
            articlenum = articlenum + 1

            print("Added article "+str(articlenum) +" of folder "+folder)

        print("*****Folder "+folder+" completed")


    mydataframe.to_csv('data.csv')

main()