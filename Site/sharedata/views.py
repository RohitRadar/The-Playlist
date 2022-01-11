from sys import path_importer_cache
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

def sharedata(request,userprofile):
    try:
        user = userprofile
        path = "assets/media/"+user+"/csv/monthly.csv"
        liked = pd.read_csv(path, sep=",")
        sorted = liked.sort_values(by=["Year"], ascending=False)
        start = sorted.iloc[0,3]
        stop = sorted.iloc[len(sorted["Year"])-1,3]
        month = ["Dec","Nov","Oct","Sep","Aug","Jul","Jun","May","Apr","Mar","Feb","Jan"]
        monthcorrect =  ["December","November","October","September","August","July","June","May","April","March","February","January"]
        yearcombine = []
        yearcombinezip = []
        for k in range(0,start-stop+1):
            i = start-k
            monthzip = []
            linkzip = []
            for j in month:
                a = sorted[sorted["Year"]==i]
                b = a[a["Month"]==j]
                if len(b["Month"]!=0):
                    c = b.sort_values(by=["Count/Month"], ascending=False)
                    monthzip.append(monthcorrect[month.index(j)])
                    linkzip.append(c.iloc[0,2])
            yearcombine.append(i)
            yearcombinezip.append(zip(monthzip,linkzip))
        totalzip = zip(yearcombine, yearcombinezip)
        return render(request,'sharedata.html',{'list1':totalzip,'userprofile':user})
    except:
        err = {'prof':99,'userprofile':user}
        return render(request,'sharedata.html',err)   
    
def shareplaylist(request, userprofile, year, month):
    try:
        user = userprofile
        songs = pd.read_csv("assets/media/"+user+"/csv/monthly.csv", sep=",")
        songs = songs[songs["Year"]==year]
        songs=songs[songs["Month"]==month[0:3]]
        sorted = songs.sort_values(by=["Count/Month"], ascending=False)
        song = list(sorted["Song"])
        artist = list(sorted["Artist"])
        link = list(sorted["Link"])
        total = list(sorted["Count/Month"])
        sorted = zip(song,artist,link,total)
        return render(request,'sharedplaylist.html',{'list1':sorted,'month':month,'year':year,'userprofile':user})
    except:
        err = {'prof':99,'userprofile':user}
        return render(request,'sharedata.html',err)   

def sharesong(request, userprofile):
    try:
        user = userprofile
        path = "assets/media/"+user+"/csv/songs.csv"
        liked = pd.read_csv(path, sep=",")
        sorted = liked.sort_values(by=["Total"], ascending=False)
        song = list(sorted["Song"])
        artist = list(sorted["Artist"])
        link = list(sorted["Link"])
        total = list(sorted["Total"])
        sorted = zip(song,artist,link,total)
        return render(request,'sharesongs.html',{'list1':sorted,'userprofile':user})
    except:
        err = {'prof':99,'userprofile':user}
        return render(request,'sharedata.html',err)   

def shareartist(request, userprofile):
    try:
        user = userprofile
        path = "assets/media/"+user+"/csv/artists.csv"
        liked = pd.read_csv(path, sep=",")
        sorted = liked.sort_values(by=["Total"], ascending=False)
        artist = list(sorted["Artist"])
        link = list(sorted["Link"])
        total = list(sorted["Total"])
        sorted = zip(artist,link,total)
        return render(request,'shareartists.html',{'list1':sorted,'userprofile':user})
    except:
        err = {'prof':99,'userprofile':user}
        return render(request,'sharedata.html',err)   