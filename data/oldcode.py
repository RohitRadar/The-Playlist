from os import listdir
from os.path import isfile, join
import urllib.request
import pandas as pd
import csv
from bs4 import BeautifulSoup
import codecs
import json

def process(user):
    try:
        months = {"01":"Jan","02":"Feb","03":"Mar","04":"Apr","05":"May","06":"Jun","07":"Jul","08":"Aug","09":"Sep","10":"Oct","11":"Nov","12":"Dec"}
        file1 = open('assets/media/'+user+'/csv/monthly.csv','w', newline='', encoding="utf-8")
        writer = csv.writer(file1)
        writer.writerow(['Song', 'Artist', 'Link', 'Year', 'Month','Count/Month'])
        watch = json.load(open('assets/media/'+user+"/html/Takeout/YouTube and YouTube Music/history/watch-history.json", encoding="utf-8"))
        i=0
        k=len(watch)-1
        artistmain = {}
        dictnot = {}
        while(i<k):
            dictmonth = {}
            month = months[watch[i]["time"][5:7]]
            year = watch[i]["time"][0:4]
            while(months[watch[i]["time"][5:7]]==month):
                try:
                    titlelist = watch[i]["title"].split(" ")
                    artistlist = watch[i]["subtitles"][0]["name"].split(" ")
                    song = watch[i]["title"][8:]
                    link = watch[i]["titleUrl"][-11:]
                    artist = watch[i]["subtitles"][0]["name"]
                    if watch[i]["header"]== "YouTube Music":
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "Official" in titlelist and "Music" in titlelist and "Video" in titlelist and "Trailer" not in titlelist and "Trailer" not in titlelist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "Official" in titlelist and "Video" in titlelist and "Trailer" not in titlelist and "(Trailer)" not in titlelist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "Official" in titlelist and "Music" in titlelist and "Trailer" not in titlelist and "Trailer" not in titlelist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "-" in artistlist and "Topic" in artistlist:
                        if artist not in artistlist:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "VEVO" in artistlist or "vevo" in artistlist or "VEVO"==artistlist[0][-4:] or "Music" in artistlist or "music" in artistlist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif watch[i]["subtitles"][0]["name"] in artistmain:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "Music" in titlelist and "[Official" in titlelist and "Video]" in titlelist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "Music" in titlelist and "(Official" in titlelist and "Video)" in titlelist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    else:
                        if song not in dictnot:
                            dictnot[song]=[artist,link,year,month,1]
                        else:
                            dictnot[song][4] = dictnot[song][4] + 1 
                except:
                    a=0
                i=i+1
                if i==k:
                    break
            for j in dictmonth:
                writer.writerow([j,dictmonth[j][0],dictmonth[j][1],year,month,dictmonth[j][2]])
        for j in dictnot:
            if dictnot[j][0] in artistmain:
                writer.writerow([j,dictnot[j][0], dictnot[j][1],dictnot[j][2],dictnot[j][3], dictnot[j][4]])
        file1.close()
    except:     
        watch = codecs.open('assets/media/'+user+"/html/Takeout/YouTube and YouTube Music/history/watch-history.html", "r", 'utf-8')
        soup = BeautifulSoup(watch.read(), 'lxml')
        total = soup.findAll('div', attrs = {'class':'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'})
        totalheader = soup.findAll('p', attrs = {'class':'mdl-typography--title'})
        file1 = open('assets/media/'+user+'/csv/monthly.csv','w', newline='', encoding="utf-8")
        writer = csv.writer(file1)
        writer.writerow(['Song', 'Artist', 'Link', 'Year', 'Month','Count/Month'])
        i=0
        artistmain = {}
        dictnot = {}
        tot = len(total)-1
        while (i<tot):
            dictmonth = {}
            dates = str(total[i].text)
            date = dates.split(",")
            dates = date[-3].split(' ')
            year = date[-2]
            month = dates[-2][-3:]
            monthfind = month
            while (month==monthfind):
                try:
                    titlelist = total[i].findAll('a')[0].text.split(" ")
                    artistlist = total[i].findAll('a')[1].text.split(" ")
                    song = total[i].findAll('a')[0].text
                    artist = total[i].findAll('a')[1].text
                    link = str(total[i].findAll('a')[0]['href'])[-11:]
                    if totalheader[i].text == "Youtube Music":
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "Official" in titlelist and "Music" in titlelist and "Video" in titlelist and "Trailer" not in titlelist and "Trailer" not in titlelist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "Official" in titlelist and "Video" in titlelist and "Trailer" not in titlelist and "(Trailer)" not in titlelist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "Official" in titlelist and "Music" in titlelist and "Trailer" not in titlelist and "Trailer" not in titlelist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "-" in artistlist and "Topic" in artistlist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "VEVO" in artistlist or "vevo" in artistlist or "VEVO"==artistlist[0][-4:] or "Music" in artistlist or "music" in artistlist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif artist == total[i].findAll('a')[1].text in artistmain:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "Music" in titlelist and "[Official" in titlelist and "Video]" in titlelist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    elif "Music" in titlelist and "(Official" in titlelist and "Video)" in titlelist:
                        if artist not in artistmain:
                            artistmain[artist] = 1
                        if song in dictmonth:
                            dictmonth[song][2] = dictmonth[song][2] + 1
                        else:
                            dictmonth[song] = [artist,link,1]
                    else:
                        if song not in dictnot:
                            dictnot[song]=[artist,link,year,month,1]
                        else:
                            dictnot[song][4] = dictnot[song][4] + 1 
                except:
                    z=1
                dates = str(total[i].text)
                date = dates.split(",")
                dates = date[-3].split(' ')
                year = date[-2]
                monthfind = dates[-2][-3:]
                i=i+1
                if i==tot:
                    break
            for j in dictmonth:
                writer.writerow([j,dictmonth[j][0],dictmonth[j][1],year,month,dictmonth[j][2]])
        for j in dictnot:
            if dictnot[j][0] in artistmain:
                writer.writerow([j,dictnot[j][0], dictnot[j][1],dictnot[j][2],dictnot[j][3], dictnot[j][4]])
        file1.close()
    file2 = open('assets/media/'+user+'/csv/songs.csv','w',newline='', encoding="utf-8")
    writer = csv.writer(file2)
    writer.writerow(['Song','Artist', 'Link','Total'])
    watched = pd.read_csv('assets/media/'+user+"/csv/monthly.csv", sep=",")
    watch = list(watched["Link"])
    dict1 = {}
    i=0
    j = len(watch)-1
    while (i<j):
        if watch[i] not in dict1:
            dict1[watch[i]] = watched.iloc[i,5]
        else:
            dict1[watch[i]] = dict1[watch[i]]+ watched.iloc[i,5]
        i=i+1
    for i in dict1:
        writer.writerow([watched.iloc[watch.index(i),0],watched.iloc[watch.index(i),1],i,dict1[i]])
    file2.close()
    file3 = open('assets/media/'+user+'/csv/artists.csv','w',newline='', encoding="utf-8")
    writer = csv.writer(file3)
    writer.writerow(['Artist', 'Link','Total'])
    art = pd.read_csv('assets/media/'+user+"/csv/songs.csv", sep=",")
    artist = list(art["Artist"])
    dict1 = {}
    j=0
    for i in artist:
        if i not in dict1:
            dict1[i] = art.iloc[j,3]
        else:
            dict1[i] = dict1[i] + art.iloc[j,3]
        j=j+1
    for i in dict1:
        writer.writerow([art.iloc[artist.index(i),1],art.iloc[artist.index(i),2],dict1[i]])
    file3.close()
"""
    path = "assets/images/"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    vidpath = 'assets/media/'+user+"/csv/songs.csv" 
    videos = pd.read_csv(vidpath, sep=",")
    like = list(videos["Link"])
    list1 = []
    for i in like:
        try:
            if i not in list1:
                list1.append(i)
                link = "http://img.youtube.com/vi/" + i + "/hqdefault.jpg"
                name = i + ".jpg"
            if name not in onlyfiles:
                urllib.request.urlretrieve(link,path+name)
        except:
            continue
"""
