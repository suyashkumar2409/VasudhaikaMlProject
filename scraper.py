from bs4 import BeautifulSoup
import requests
import os
import codecs
def getPath():
    return "/home/vasudhaika/Desktop/classifiednews"

def pathconcat(path1,folder):
    return path1+ "/" + folder

def adddirectory(currpath):

    newpath = currpath

    if not os.path.exists(newpath):
        os.makedirs(newpath)


def makefile(name,body,currpath):
    file = codecs.open(pathconcat(currpath,name), "a", "utf-8")
    #file = os.open(pathconcat(currpath,name), os.O_APPEND)
    file.write(body)
    file.close()

def urlconcat(base,sub):
    return base+sub

def agrimoneymain():
    startingurl = "http://www.agrimoney.com/1/commodities/"

    home = requests.get(startingurl)

    homesoup = BeautifulSoup(home.content)
    hometable = homesoup.find_all('table', 'cat_under')[0]

    for a in hometable.find_all('a', 'minicat'):
        commodity = requests.get(a.attrs['href'])  # .text.encode('utf-8').decode('ascii', 'ignore')
        commoditysoup = BeautifulSoup(commodity.content)
        commodityname = commoditysoup.find_all('font', 'whiteheadlarge')[0].getText()

        if commodityname == "Commodities":
            continue

        print("Scraping Commodity " + commodityname)
        currpath = pathconcat(getPath(), commodityname)
        adddirectory(currpath)

        newslist = []
        newslist.append(commoditysoup.find_all('a', 'brownlinklarge')[0].attrs['href'])

        for link in commoditysoup.find_all('a', 'brownlinkmedium'):
            newslist.append(link.attrs['href'])

        articlenum = 0
        for link in newslist:
            newspage = requests.get(link)  # .text.encode('utf-8').decode('ascii', 'ignore')
            newspagesoup = BeautifulSoup(newspage.content)

            title = newspagesoup.find_all('font', 'blackheadlarge')[0].getText()

            plist = newspagesoup.find_all('font', 'calib')[0].find_all('p')
            # print(len(plist))
            body = title
            for p in plist:
                body = body + " " + p.text
                # print(p.text)
            print("************Scraping article " + str(articlenum) + " of " + str(len(newslist)) + " articles")
            makefile(str(articlenum) + ".txt", body, currpath)

            articlenum = articlenum + 1


def farmsmain():
    startingurl = "http://www.farms.com/"

    home = requests.get(startingurl)
    homesoup = BeautifulSoup(home.content)

    allcrops = homesoup.find_all('div','Leftpanel')[0].find_all('li','p4')[0].find_all('a', 'Leftlinks')

    avoidcrops = ['Field Guide','Yield Data Centre']

    for crop in allcrops:
        cropname = crop.text
        if cropname not in avoidcrops:
            foldername = cropname + "_farms"

            currpath = pathconcat(getPath(),foldername)
            adddirectory(currpath)

            newssite = requests.get(urlconcat(startingurl, crop['href']))
            newssitesoup = BeautifulSoup(newssite.content)

            newssite = requests.get((newssitesoup.find_all('div',id = 'ctl00_more_link_SubPage')[0].find_all('a')[0])['href'])
            newssitesoup = BeautifulSoup(newssite.content)

            table = newssitesoup.find_all('table','tableBorderthin')[0]
            tr = table.find_all('tr')[1]

            #alllinks = tr.find_all('a')

            allnews = tr.find_all('div',style = 'padding: 2px 0px; display: block;')

            articlenum = 0


            for news in allnews:
                newslink = news.a['href']
                newspage = requests.get(newslink)
                newspagesoup =  BeautifulSoup(newspage)

                allparas = newspagesoup.find_all('table','tableBorderthin')[0].find_all('tr')[1].find_all('p')

                totaltext = ""
                for para in allparas:
                    totaltext = totaltext + para.text

                makefile(str(articlenum) + '.txt', totaltext, currpath)
                
            nextpage =






def main(site):

    ###########Code for agrimoney##########
    if site == 'agrimoney':
        agrimoneymain()
    elif site == 'farms':
        farmsmain()

main('farms')