from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import TaksForm 
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
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
                return  redirect("index")
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
            return redirect("index") 

@login_required
def taskPending(request):
    task = Task.objects.filter(user=request.user, dateCompleted__isnull=True)

    return render(request, "taskPending.html",{
        "tasks" : task
    })

@login_required 
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
            return  redirect("taskPending")
        except ValueError:
            return render(request, 'createTask.html', {
                "form":TaksForm,
                "error":"please provide valide data"
            })

@login_required
def taskDetail(request, taskId):
    if(request.method == "GET"):
        task = get_object_or_404(Task,pk=taskId, user=request.user)
        form = TaksForm(instance=task )
        return render(request, "taskDetail.html",{
            "tasks": task,
            "form" : form
        })
    else:
        try:
                
            task = get_object_or_404(Task,pk=taskId, user=request.user)
            form = TaksForm(request.POST, instance=task)
            form.save()
            return redirect('taskPending')
        except ValueError:
            return render(request, "taskDetail.html",{
                "tasks": task,
                "form" : form,
                "error" : "please provide valide data"
            })

@login_required
def completeTask(request, taskId):
    task = get_object_or_404(Task,pk=taskId, user=request.user)
    if request.method == "POST":
        task.dateCompleted = timezone.now()
        task.save()
        return redirect("taskComplete")

@login_required
def deleteTask(request, taskId):
    task = get_object_or_404(Task,pk=taskId, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("taskPending")

@login_required
def taskComplete(request):
    task = Task.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')

    return render(request, "taskComplete.html",{
        "tasks" : task
    })
