from django.shortcuts import render, HttpResponseRedirect
import pandas as pd
from django.contrib import messages

def songs(request):
	if request.user.is_authenticated:
		user = request.user.username
		try:
			path = "assets/media/"+user+"/csv/songs.csv"
			liked = pd.read_csv(path, sep=",")
			sorted = liked.sort_values(by=["Total"], ascending=False)
			song = list(sorted["Song"])
			artist = list(sorted["Artist"])
			link = list(sorted["Link"])
			total = list(sorted["Total"])
			sorted = zip(song,artist,link,total)
			return render(request,'songs.html',{'list1':sorted})
		except:
			messages.error(request,"Upload file to view your Favourite Songs")
			return render(request,'songs.html')
	else:
		return render(request,'songs.html')
#{'songs':song,'artists':artist,'links':link,'totals':total}