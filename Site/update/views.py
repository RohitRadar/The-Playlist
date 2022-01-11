from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from zipfile import ZipFile
from .import code
from django.contrib import messages
import os
import shutil

##NOT SELECTING YOUTUBE DATA FIELDS, then no need filename[0:-4] as output zip comes out as takeout
def handle_uploaded_file(request,f,user):
    loc = "assets/media/"
    path = os.path.join(loc, user)
    if os.path.exists(path):
        shutil.rmtree(path)
    try:
        filename = "Takeout.zip"
        fip = ZipFile(f,'r')
        path = 'assets/media/' + str(user) + "/"
        try:
            fip.extract(filename[0:-4]+'/YouTube and YouTube Music/history/watch-history.html',path+'html/')
        except:
            fip.extract(filename[0:-4]+'/YouTube and YouTube Music/history/watch-history.json',path+'html/')
        dir = "csv"
        new = os.path.join(path,dir)
        os.mkdir(new)  
        code.process(user)
        shutil.rmtree("assets/media/" + user + "/html")
    except:
        messages.error(request,"Watch-History.JSON not Chosen in Google Takeout")

def update(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                #messages.error(request,"Processing Data, Wait for few Moments")
                render(request,'songs.html')
                handle_uploaded_file(request,request.FILES['file'], request.user.username)
                return HttpResponseRedirect('/songs')
            else:
                return HttpResponseRedirect('/update')
        else:
            form = UploadFileForm()
        return render(request, 'update.html', {'form': form})
    else:
        return render(request, 'update.html')

#os.chmod(filePath, 0o777)
#os.remove(filePath)
#try:
        #filename = str(f.name)
    #os.rename('assets/media/'+str(user)+"/html/"+filename[0:-4],'assets/media/'+str(user)+"/html/"+"Takeout")