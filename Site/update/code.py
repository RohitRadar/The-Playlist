from os import listdir
from os.path import isfile, join
import urllib.request
import pandas as pd
import csv
from bs4 import BeautifulSoup
import codecs
import json
import aiohttp
import asyncio
import time
from apiclient.discovery import build
DEVELOPER_KEY = "AIzaSyBsYqedKSWrYMogI1cCsDn9sUieu2h6qWY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, 
                     YOUTUBE_API_VERSION,
            developerKey = DEVELOPER_KEY)
def video_details(video_id):
    song = "none"
    artist = "none"
    try:
        time.sleep(0.1)
        list_videos_byid = youtube.videos().list(id = video_id,part = "snippet").execute()
        results = list_videos_byid.get("items", [])
        cat = results[0]["snippet"]["categoryId"]
        #print(cat)
        if cat==10 or cat==24:
            song = results[0]["snippet"]["title"]
            artist = results[0]["snippet"]["channelTitle"]
    except:
        song="none"
        artist="none"
    return song,artist

async def get_song(session, url):
    dictlink = {}
    async with session.get(url) as resp:
        try:
            info = await resp.read()
            info = json.loads(info)
            dictlink[info["title"]]=[info["author_name"],url[-11:]]
        except:
            a=0
    return dictlink
    
async def main(urls):
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []
        for url in urls:
            #url = "https://noembed.com/embed?url=https://youtube.com/watch?v="+url
            url = "https://www.youtube.com/oembed?url=https://youtube.com/watch?v="+url
            tasks.append(asyncio.ensure_future(get_song(session, url)))
        dictlink = await asyncio.gather(*tasks)
        #print(dictlink)
    return dictlink
def classifier(dictmonth,dictnot,song,artist,link,year,month,artistmain,watch,i):
    if watch[i]["header"]== "YouTube Music":
        if artist not in artistmain:
            artistmain[artist] = 1
        if song in dictmonth:
            dictmonth[song][2] = dictmonth[song][2] + 1
        else:
            dictmonth[song] = [artist,link,1]
    elif "trailer" not in song.lower() and "tutorial" not in song.lower():
        if "audio" in song.lower() or "full album" in song.lower() or "(OST" in song or " OST" in song or "soundtrack" in song.lower() or "official video" in song.lower() or "official music" in song.lower():
            if song in dictmonth:
                dictmonth[song][2] = dictmonth[song][2] + 1
            else:
                dictmonth[song] = [artist,link,1]
        elif "topic" in artist.lower() or "vevo" in artist.lower() or "music" in artist.lower():
            if song in dictmonth:
                dictmonth[song][2] = dictmonth[song][2] + 1
            else:
                dictmonth[song] = [artist,link,1]
        elif artist in artistmain:
            if song in dictmonth:
                dictmonth[song][2] = dictmonth[song][2] + 1
            else:
                dictmonth[song] = [artist,link,1]
        else:
            if song not in dictnot:
                dictnot[song]=[artist,link,year,month,1]
            else:
                dictnot[song][4] = dictnot[song][4] + 1 
    else:
        a=0

def classifier1(dictmonth,dictnot,song,artist,link,year,month,artistmain,totalheader,i):
    if totalheader[i].text == "Youtube Music":
        if artist not in artistmain:
            artistmain[artist] = 1
        if song in dictmonth:
            dictmonth[song][2] = dictmonth[song][2] + 1
        else:
            dictmonth[song] = [artist,link,1]
    elif "trailer" not in song.lower() and "tutorial" not in song.lower():
        if "audio" in song.lower() or "full album" in song.lower() or "(OST" in song or " OST" in song or "soundtrack" in song.lower() or "official video" in song.lower() or "official music" in song.lower():
            if song in dictmonth:
                dictmonth[song][2] = dictmonth[song][2] + 1
            else:
                dictmonth[song] = [artist,link,1]
        elif "topic" in artist.lower() or "vevo" in artist.lower() or "music" in artist.lower():
            if song in dictmonth:
                dictmonth[song][2] = dictmonth[song][2] + 1
            else:
                dictmonth[song] = [artist,link,1]
        elif artist in artistmain:
            if song in dictmonth:
                dictmonth[song][2] = dictmonth[song][2] + 1
            else:
                dictmonth[song] = [artist,link,1]
        else:
            if song not in dictnot:
                dictnot[song]=[artist,link,year,month,1]
            else:
                dictnot[song][4] = dictnot[song][4] + 1 
    else:
        a=0


def process(user):
    try:
        months = {"01":"Jan","02":"Feb","03":"Mar","04":"Apr","05":"May","06":"Jun","07":"Jul","08":"Aug","09":"Sep","10":"Oct","11":"Nov","12":"Dec"}
        file1 = open('assets/media/'+user+'/csv/monthly.csv','w', newline='', encoding="utf-8")
        writer = csv.writer(file1)
        writer.writerow(['Song', 'Artist', 'Link', 'Year', 'Month','Count/Month'])
        watch = json.load(open('assets/media/'+user+"/html/Takeout/YouTube and YouTube Music/history/watch-history.json", encoding="utf-8"))
        i=0
        z=len(watch)-1
        artistmain = {}
        dictnot = {}
        while(i<z):
            dictmonth = {}
            urls={}
            month = months[watch[i]["time"][5:7]]
            year = watch[i]["time"][0:4]
            while(months[watch[i]["time"][5:7]]==month):
                if watch[i]["header"] != "Youtube" and watch[i]["title"] !="Visited YouTube Music":
                    try:
                        try:
                            song = watch[i]["title"][8:]
                            link = watch[i]["titleUrl"][-11:]
                            artist = watch[i]["subtitles"][0]["name"]
                            classifier(dictmonth,dictnot,song,artist,link,year,month,artistmain, watch,i)
                        except:    
                            link = watch[i]["titleUrl"][-11:]
                            urls[link] = i
                    except:
                        a=0
                i=i+1
                if i==z:
                    break
            if len(urls)>0:
                b=0
                while(b==0):
                    try:
                        dictlink = asyncio.run(main(urls))
                        b=1
                    except:
                        b=0
                        time.sleep(1)
            for j in dictlink:
                for k in j:
                    classifier(dictmonth,dictnot,k,j[k][0],j[k][1],year,month,artistmain,watch, urls[j[k][1]])
            for j in dictmonth:
                if " - Topic" in dictmonth[j][0]:
                    writer.writerow([j,dictmonth[j][0][:-7],dictmonth[j][1],year,month,dictmonth[j][2]])
                else:
                    writer.writerow([j,dictmonth[j][0],dictmonth[j][1],year,month,dictmonth[j][2]])
        for j in dictnot:
            if dictnot[j][0] in artistmain or dictnot[j][4]>3:
                song,artist=video_details(dictnot[j][1])
                if song!="none" and artist!="none":
                    if " -Topic" in artist:
                        writer.writerow([song,artist[:-7], dictnot[j][1],dictnot[j][2],dictnot[j][3], dictnot[j][4]])
                    else:
                        writer.writerow([song,artist, dictnot[j][1],dictnot[j][2],dictnot[j][3], dictnot[j][4]])
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
        artistmain={}
        dictnot = {}
        tot = len(total)-1
        while (i<tot):
            dictmonth = {}
            urls={}
            dates = str(total[i].text)
            date = dates.split(",")
            try:
                dates = date[-3].split(' ')
                year = date[-2]
                month = dates[-2][-3:]
            except:
                dates = date[-2].split(' ')
                year = dates[-1]
                month=dates[-2]
            monthfind = month
            while (month==monthfind):
                try:
                    song = total[i].findAll('a')[0].text
                    artist = total[i].findAll('a')[1].text
                    link = str(total[i].findAll('a')[0]['href'])[-11:]
                    classifier1(dictmonth,dictnot,song,artist,link,year,month,artistmain, totalheader,i)
                except:
                    try:
                        link = str(total[i].findAll('a')[0]['href'])[-11:]
                        urls[link]=i
                    except:
                        a=0
                i=i+1
                if i==tot:
                    break
                dates = str(total[i].text)
                date = dates.split(",")
                try:
                    dates = date[-3].split(' ')
                    year = date[-2]
                    monthfind = dates[-2][-3:]
                except:
                    dates = date[-2].split(' ')
                    year = dates[-1]
                    monthfind=dates[-2]
            if len(urls)>0:
                b=0
                while(b==0):
                    try:
                        dictlink = asyncio.run(main(urls))
                        b=1
                    except:
                        time.sleep(1)
                        b=0
            for j in dictlink:
                for k in j:
                    classifier1(dictmonth,dictnot,k,j[k][0],j[k][1],year,month,artistmain,totalheader, urls[j[k][1]])
            for j in dictmonth:
                if " - Topic" in dictmonth[j][0]:
                    writer.writerow([j,dictmonth[j][0][:-7],dictmonth[j][1],year,month,dictmonth[j][2]])
                else:
                    writer.writerow([j,dictmonth[j][0][:-7],dictmonth[j][1],year,month,dictmonth[j][2]])
        for j in dictnot:
            if dictnot[j][0] in artistmain or dictnot[j][4]>3:
                song,artist=video_details(dictnot[j][1])
                if song!="none" and artist!="none":
                    writer.writerow([song,artist, dictnot[j][1],dictnot[j][2],dictnot[j][3], dictnot[j][4]])
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


