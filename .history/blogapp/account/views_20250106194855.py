from django.shortcuts import render,redirect
from django.contrib.auth import authenticate

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "account/login.html", {
                "error": "Kullanıcı adı ya da şifre yanlış"
            })
    return render(request, "account/login.html")
def register(request):
    return render(request, "account/register.html")
def logout(request):
    return redirect("home")