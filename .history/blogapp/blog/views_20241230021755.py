from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from blog.models import tb_general
from blog.models import tb_home
from blog.models import tb_away

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
        },
        {
            "league": "None",
        }
    ],
    "seasons": [{"season": f"{year}/{year+1}"} for year in range(datetime.now().year, 1999, -1)] + [{"season": "None"}],
}
def index(request):
    return render(request, "blog/index.html")

def collect_data(request):
    # Dropdown seçimlerini al
    selected_league = request.GET.get('league', None)
    selected_season = request.GET.get('season', None)

    tb_general = tb_general.objects.all()

    # Filtre uygula (dropdown seçimlerine göre)
    if selected_league and selected_league != "None":
        tb_general = tb_general.filter(league=selected_league)  # Eğer "league" modelde varsa

    if selected_season and selected_season != "None":
        season_year = selected_season.split('/')[0]
        tb_general = tb_general.filter(season=season_year)

    # Dinamik olarak oyuncu bilgilerini getirin
    data = []
    for match in tb_general:
        home_players = tb_home.objects.filter(match_ID=match.match_ID)
        away_players = tb_away.objects.filter(match_ID=match.match_ID)

        data.append({
            "match": match,
            "home_players": list(home_players),
            "away_players": list(away_players),
        })
    context = {
        "leagues": data["leagues"],
        "seasons": data["seasons"],
        "data": data,
        "selected_league": selected_league if selected_league != "None" else None,
        "selected_season": selected_season if selected_season != "None" else None,
    }
    return render(request, "blog/collect_data.html", context)

def predict(request):
    return render(request, "blog/predict.html")