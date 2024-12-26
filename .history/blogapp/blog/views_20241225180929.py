from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "blog/index.html")

def collect_data(request):
    return render(request, "blog/collect_data.html")

def predict(request):
    return render(request, "blog/predict.html")