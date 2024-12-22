from django.shortcuts import render, redirect
from django.conf import settings

### DEC
from django.template.loader import get_template
from django.template import Context

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
import requests

# Create your views here.

###
#restapi_host = "127.0.0.1:5000"

def getpipelines():
    pipelinelist = []
    try:
        collected = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/')
        if collected.status_code == 200:
            # parse the JSON response and retrieve the pipeline topology
            pipelines = collected.json()["payload"]["pipelines"]
            for pipeline in pipelines:
                pipelinelist.append(pipeline["name"]) 
    except:
        pipelinelist = []            
    return pipelinelist


def view_base(request):  
    context = {}
    context["all_pipelines"] = getpipelines()  
    return render(request,'active_main.html',context)
    

def view_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request = request,
                  template_name = "app_login.html",
                  context={"form":form})

def view_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')

