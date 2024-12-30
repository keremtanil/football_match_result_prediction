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

    table_data = tb_general.objects.all()
    # Filtre uygula (dropdown seçimlerine göre)
    if selected_league and selected_league != "None":
        table_data = table_data.filter(league=selected_league)  # Eğer "league" modelde varsa

    if selected_season and selected_season != "None":
        season_year = selected_season.split('/')[0]
        table_data = table_data.filter(season=season_year)

    # İkinci tablodan futbolcu bilgilerini al
    player_data = tb_homePlayers.objects.all()
    if selected_league and selected_league != "None":
        player_data = player_data.filter(league=selected_league)
    if selected_season and selected_season != "None":
        season_year = selected_season.split('/')[0]
        player_data = player_data.filter(season=season_year)

    # Tabloları birleştir
    merged_data = []
    for match in table_data:
        players = player_data.filter(season=match.season, league=match.league)
        prepared_players = []
        for player in players:
            prepared_players.append({
                "name": player.name,
                "national": player.national,
                "age": player.age,
            })
        merged_data.append({
            "match": match,
            "players": prepared_players,  # Burada oyuncu bilgilerini organize ettik
        })
    context = {
        "leagues": data["leagues"],
        "seasons": data["seasons"],
        "merged_data": merged_data,
        "selected_league": selected_league if selected_league != "None" else None,
        "selected_season": selected_season if selected_season != "None" else None,
    }
    return render(request, "blog/collect_data.html", context)

def predict(request):
    return render(request, "blog/predict.html")