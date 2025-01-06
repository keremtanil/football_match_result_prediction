from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

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
    if request.method == "POST":
        name = request.POST["name"]
        surname = request.POST["surname"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", {
                    "error": "Kullanıcı adı kullanılıyor.",
                    "name": name,
                    "surname": surname,
                    "email": email,
                    "username": username
                })
            else :
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html", {
                        "error": "Kullanıcı adı kullanılıyor.",
                        "name": name,
                        "surname": surname,
                        "email": email,
                        "username": username
                    })
                else:
                    user = User.objects.create_user(name=name,surname=surname,email=email,username=username,password=password)
                    user.save()
                    return redirect("login")
        else:
            return render(request, "account/register.html", {
                "error": "Parola eşleşmiyor.",
                "name": name,
                "surname": surname,
                "email": email,
                "username": username
            })

    return render(request, "account/register.html")
def logout(request):
    return redirect("home")