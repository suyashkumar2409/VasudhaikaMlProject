from bs4 import BeautifulSoup
import requests
import os

def getPath():
    return "/home/vasudhaika/Desktop/classifiednews"

def pathconcat(path1,folder):
    return path1+ "/" + folder

def adddirectory(currpath):
    newpath = currpath

    if not os.path.exists(newpath):
        os.makedirs(newpath)


def makefile(name,body,currpath):
    file = open(pathconcat(currpath,name), "a")
    file.write(body)
    file.close()

def main(site):

    ###########Code for agrimoney##########
    if site == 'agrimoney':
        startingurl = "http://www.agrimoney.com/1/commodities/"

        home = requests.get(startingurl)

        homesoup = BeautifulSoup(home.content)
        hometable = homesoup.find_all('table','cat_under')[0]

        for a in hometable.find_all('a','minicat'):
            commodity = requests.get(a.attrs['href'])
            commoditysoup = BeautifulSoup(commodity.content)
            commodityname = commoditysoup.find_all('font','whiteheadlarge')[0].getText()

            print("Scraping Commodity "+commodityname)
            currpath = pathconcat(getPath(),commodityname)
            adddirectory(currpath)

            newslist = []
            newslist.append(commoditysoup.find_all('a','brownlinklarge')[0].attrs['href'])

            for link in commoditysoup.find_all('a','brownlinkmedium'):
                newslist.append(link.attrs['href'])

            articlenum = 0
            for link in newslist:
                newspage = requests.get(link)
                newspagesoup = BeautifulSoup(newspage.content)

                title = newspagesoup.find_all('font','blackheadlarge')[0].getText()

                plist = newspagesoup.find_all('font','calib')[0].find_all('p')
               # print(len(plist))
                body = title
                for p in plist:
                    body = body + str(p.getText())
                   # print(p.text)
                print("************Scraping article "+str(articlenum)+" of "+ str(len(newslist))+" articles")
                makefile(str(articlenum) + ".txt",body,currpath)

                articlenum = articlenum + 1


main('agrimoney')