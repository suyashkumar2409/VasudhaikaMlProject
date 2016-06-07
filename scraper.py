from bs4 import BeautifulSoup
import requests
import os
import codecs
import re
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
    #print(body)
    file.close()

def urlconcat(base,sub):
    return base+sub

def updatelog(currpath, pagenum, articlenum, read):
    filename = pathconcat(currpath, "log.txt")
    if not os.path.exists(filename):
        articlenum = 0
        pagenum = 0
        file = codecs.open(filename, "w", "utf-8")
        body = str(pagenum)+ "\n" + str(articlenum)
        file.write(body)
        file.close()

        print("\n\n%%%%%%%%Creating Log File\n")

        return pagenum, articlenum
    elif read==False:
        file = codecs.open(filename, "w", "utf-8")
        body = str(pagenum) + "\n" + str(articlenum)
        file.write(body)
        file.close()
        print("\n\n%%%%%%%%Updating Log File\n")

        return pagenum, articlenum

    else:
        file = codecs.open(filename, "r", "utf-8")
        content = file.readlines()
        #print(content)
        pagenum = int(content[0].replace('\n', ''))
        articlenum = pagenum*50
        print("\n\n%%%%%%%%Reading Log File\n")
        return pagenum, articlenum

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

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title'] :
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))) :
        return False
    return True

def farmsmain():
    startingurl = "http://www.farms.com/"

    home = requests.get(startingurl)
    homesoup = BeautifulSoup(home.content)

    print("Going to farms.com")

    allcrops = homesoup.find_all('div','Leftpanel')[0].find_all('li','p4')[0].find_all('a', 'Leftlinks')

    avoidcrops = ['Field Guide','Yield Data Centre']

    for crop in allcrops:
        cropname = crop.text
        if cropname not in avoidcrops:
            foldername = cropname + "_farms"

            print("########Scraping commodity "+ cropname)

            currpath = pathconcat(getPath(),foldername)
            adddirectory(currpath)

            newssite = requests.get(urlconcat(startingurl, crop['href']))
            newssitesoup = BeautifulSoup(newssite.content)

            newssite = requests.get(urlconcat(startingurl,newssitesoup.find_all('div', id='ctl00_more_link_SubPage')[0].find_all('a')[0]['href']))
            newssitesoup = BeautifulSoup(newssite.content)

            ####################The actual site with all news articles###########################################################################
            morepages = True
            articlenum  = 0
            pagenum = 0

            currpagenum = 0
            pagenum, articlenum = updatelog(currpath, pagenum, articlenum, read=True)
            #print(pagenum)
            #print(currpagenum)

            while morepages:
                #print("ina loop")
                if currpagenum == pagenum:
                    table = newssitesoup.find_all('table','tableBorderthin')[0]
                    tr = table.find_all('tr')[1]
                  #  print(tr)
                    #alllinks = tr.find_all('a')

                    allnews = tr.find_all('div',style = 'padding: 2px 0px; display: block;')
                  #  print(allnews)
                    #pagenum, articlenum = updatelog(currpath, pagenum, articlenum, read=True)

                    for news in allnews:
                        newslink = news.a['href']
                        newspage = requests.get(urlconcat(startingurl,newslink))
                        newspagesoup =  BeautifulSoup(newspage.content)

                        totaltext = newspagesoup.find_all('table','tableBorderthin')[0].text
                        #print(allparas)
                        #allparas = filter(visible, allparas)

                        #for para in allparas:
                         #   totaltext = totaltext + para

                        makefile(str(articlenum) + '.txt', totaltext, currpath)

                        print("****************Scraping article "+str(articlenum)+" on page "+str(pagenum))
                        #pagenum, articlenum = updatelog(currpath, articlenum, pagenum)


                        articlenum = articlenum + 1

                nextpageanchors = newssitesoup.find_all('div',id='dnn_ctr2314_ShowNewsUpdated_dvNewsAnchor')[0].find_all('a')
                nextpage = None
                for anchor in nextpageanchors:
                    if anchor.text == ' > ':
                        nextpage = anchor['href']
                #print((nextpage))
                if nextpage:
                    newssite = requests.get((nextpage))
                    newssitesoup = BeautifulSoup(newssite.content)
                    if currpagenum == pagenum:
                        pagenum = pagenum + 1
                        pagenum, articlenum = updatelog(currpath, pagenum, articlenum, read = False)
                    currpagenum = currpagenum+1

                else:
                    morepages = False


def main(site):

    ###########Code for agrimoney##########
    if site == 'agrimoney':
        agrimoneymain()
    elif site == 'farms':
        farmsmain()

main('farms')