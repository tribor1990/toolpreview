from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import Newjobform
from django.core.files import File
from django.http import JsonResponse
from django.core import serializers
from io import BytesIO
from zipfile import ZipFile
from django.core.files.storage import default_storage    
from django.core.files.base import ContentFile
import os, sys
from .models import  Userjob
# Create your views here.
def home(request):
    return render(request, 'ordertool/home.html')


def signupuser(request):
    #Show Signupform on GET
    if request.method == 'GET':
        return render(request, 'ordertool/signupuser.html', {'form':UserCreationForm()})
    else:
        #Create USER on POST
        if request.POST['password1'] == request.POST['password2']:
            try:

                user = User.objects.create_user(request.POST['username'], password=request.POST['password2'])
                user.save()
                login(request, user)
                return redirect('useroverview')

            except IntegrityError:
                return render(request, 'ordertool/signupuser.html', {'form':UserCreationForm(), 'error': 'Username already taken! Please chose a new username!'})

        else:
            return render(request, 'ordertool/signupuser.html', {'form':UserCreationForm(), 'error': 'Passwords did not match'})


def loginuser(request):
     
    if request.method == 'GET':
        return render(request, 'ordertool/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'ordertool/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match!'})
        else:
            login(request, user)
            return redirect('useroverview')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')






def useroverview(request):
    jobs = Userjob.objects.filter(jobcreator=request.user)
    return render(request, 'ordertool/useroverview.html', {'jobs' : jobs}) 


def viewjob(request, job_pk):

    job = get_object_or_404(Userjob, pk=job_pk)
    return render(request, 'ordertool/viewjob.html', {'job' : job}) 



def newjob(request):
    if request.method == 'GET':
        return render(request, 'ordertool/neworder.html', {'form':Newjobform()})


    else:
        if request.is_ajax and request.method == "POST":
            form = Newjobform(request.POST)
            print('_______FORM__________________')
            print(form)
            print('_______FILES________________')
            print(request.FILES)
            neworder = form.save(commit=False)
            neworder.jobcreator = request.user
            print('_________OBJECT_________')
            
            neworder.user = request.user
            #print(neworder.jobcreator)
            print(neworder.title)
            print(neworder.deadlinedate)
            print(neworder.newzip)


            files = request.FILES#.getlist('files')
            zipname = neworder.title +".zip"
            with ZipFile(zipname, 'w') as zipObj2:
                for key in request.FILES:
                    print('test:' + key)
                    print('filesize:' + str(request.FILES[key].size))
                    print('name' + request.FILES[key].name)
                    print('tmppath:' + request.FILES[key].temporary_file_path())
                  
                  
                    zipObj2.write(request.FILES[key].temporary_file_path(), request.FILES[key].name)
                   

                zipObj2.close()
                neworder.newzip = File(open(zipname, "rb"))
                neworder.save()
                neworder.idxml = neworder.id + 2000000
                neworder.save()
                #Delete tempzip
                os.remove(zipname)



            ser_instance = serializers.serialize('json', [ neworder, ])
        
            
            return JsonResponse({"neworder": ser_instance}, status=200)


        