from django.shortcuts import render
from django.http import HttpResponse

data ={
    "leagues":[
        {
            "league": "Turkey",
        },
        {
            "league": "England",
        },
        {
            "league": "Germany",
        },
        {
            "league": "Italy",
        },
        {
            "league": "Spain",
        },
        {
            "league": "France",
        }
    ],
    "seasons": [{"season": f"{year}/{year+1}"} for year in range(datetime.now().year, 1999, -1)]
}
def index(request):
    return render(request, "blog/index.html")

def collect_data(request):
    context = {
        "leagues": data["leagues"],
        "seasons": data["seasons"],
    }
    return render(request, "blog/collect_data.html", context)

def predict(request):
    return render(request, "blog/predict.html")