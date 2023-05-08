from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
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
    return render(request, "task.html")

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