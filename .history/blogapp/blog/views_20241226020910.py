from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from blog.models import tb_collect

data ={
    "leagues":[
        {
            "league": "Turkey",
        },
        {
            "league": "Premier League",
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
    # Dropdown seçimlerini al
    selected_league = request.GET.get('league', None)
    selected_season = request.GET.get('season', None)

    table_data = tb_collect.objects.all()
    # Filtre uygula (dropdown seçimlerine göre)
    if selected_league:
        table_data = table_data.filter(league=selected_league)  # Eğer "league" modelde varsa

    if selected_season:
        season_year = selected_season.split('/')[0]
        table_data = table_data.filter(season=season_year)

    context = {
        "leagues": data["leagues"],
        "seasons": data["seasons"],
        "table_data": table_data,
    }
    return render(request, "blog/collect_data.html", context)

def predict(request):
    return render(request, "blog/predict.html")