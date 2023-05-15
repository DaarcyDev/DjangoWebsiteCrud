from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import TaksForm 
from .models import Task
# Create your views here.


def home(request):
    return render(request, "home.html", {
        "form": UserCreationForm
    })


def singup(request): 

    if request.method == "GET":
        return render(request, "singup.html", {
            "form": UserCreationForm
        })
    else:
        if (request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return  redirect("task")
            except:
                return render(request, "singup.html", {
                    "form": UserCreationForm,
                    "error": "user already exist"
                })

        else:
            return render(request, "singup.html", {
                "form": UserCreationForm,
                "error": "password dont match"
            })

        print(request.POST)
        print("obteniendo datos")

def task(request):
    task = Task.objects.filter(user=request.user)

    return render(request, "task.html",{
        "tasks" : task
    })

def signout (request):
    logout(request)
    return redirect("index")


def signin(request):
    if request.method == "GET":

        return render(request,"signin.html",{
            "form":AuthenticationForm
        })
    else:
        user = authenticate(request, username = request.POST["username"], password= request.POST["password"])

        if(user is None):
 
            return render(request,"signin.html",{
                "form":AuthenticationForm,
                "error":"user or password is incorrect"
            })
        else:
            login(request, user)
            return redirect("task") 
        
def createTask(request):

    if request.method == "GET":
        return render(request, 'createTask.html', {
            "form":TaksForm
        })
    else:
        try:

            form = TaksForm(request.POST)
            newTask = form.save(commit=False )
            newTask.user = request.user
            newTask.save()
            return  redirect("task")
        except ValueError:
            return render(request, 'createTask.html', {
                "form":TaksForm,
                "error":"please provide valide data"
            })

def taskDetail(request, taskId):
    task = get_object_or_404(Task,pk=taskId)
    return render(request, "taskDetail.html",{
        "tasks": task
    })