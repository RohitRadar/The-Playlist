from django.shortcuts import render, HttpResponseRedirect
import csv
import pandas as pd
from django.contrib import messages

def artists(request):
	if request.user.is_authenticated:
		user = request.user.username
		try:
			path = "assets/media/"+user+"/csv/artists.csv"
			liked = pd.read_csv(path, sep=",")
			sorted = liked.sort_values(by=["Total"], ascending=False)
			artist = list(sorted["Artist"])
			link = list(sorted["Link"])
			total = list(sorted["Total"])
			sorted = zip(artist,link,total)
			return render(request,'artists.html',{'list1':sorted})
		except:
			messages.error(request,"Upload file to view your Favourite Artists")
			return render(request,'artists.html')
			#return HttpResponseRedirect('/update')	
	else:
		return render(request,'artists.html')
