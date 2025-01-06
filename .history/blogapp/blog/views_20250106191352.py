from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from blog.models import tb_general
from blog.models import tb_home
from blog.models import tb_away
from .forms import DateField
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from django.contrib import messages
from django import forms

data ={
    "leagues":[{"league": "Super Lig",},{"league": "Premier League",},{"league": "Bundesliga",},{"league": "Serie A",},{"league": "La Liga",},{"league": "Ligue 1",},{"league": "None",}],
    "seasons": [{"season": f"{year}-{year+1}"} for year in range(datetime.datetime.now().year -2, 2016, -1)] + [{"season": "None"}],
}
data_live ={
    "leagues":[{"league": "Super Lig",},{"league": "Premier League",},{"league": "Bundesliga",},{"league": "Serie A",},{"league": "La Liga",},{"league": "Ligue 1",}],
    "seasons": [{"season": f"{year}-{year+1}"} for year in range(datetime.datetime.now().year -2, 2016, -1)],
}
league_data = {
    "Premier League": {"id": "9", "slug": "Premier-League-Scores-and-Fixtures"},
    "Ligue 1": {"id": "13", "slug": "Ligue-1-Scores-and-Fixtures"},
    "Bundesliga": {"id": "20", "slug": "Bundesliga-Scores-and-Fixtures"},
    "Serie A": {"id": "11", "slug": "Serie-A-Scores-and-Fixtures"},
    "La Liga": {"id": "12", "slug": "La-Liga-Scores-and-Fixtures"},
    "Super Lig": {"id": "26", "slug": "Super-Lig-Scores-and-Fixtures"}
}
def index(request):
    return render(request, "blog/index.html")

def collect_data(request):
    league = {"Premier League":"ENG-m","Ligue 1":"FRA-m","Bundesliga":"GER-m","Serie A":"ITA-m","La Liga":"ESP-m","Super Lig":"TUR-m","None":"None"}
    selected_league_first = request.GET.get('league', None)
    selected_league = league.get(selected_league_first, None)
    selected_season = request.GET.get('season', None)

    general = tb_general.objects.all()

    if selected_league_first and selected_league_first != "None":
        general = general.filter(league=selected_league)

    if selected_season and selected_season != "None":
        season_year = selected_season.split('-')[0]
        general = general.filter(season=season_year)

    # Önce maksimum oyuncu sayılarını bul
    max_home_players = 0
    max_away_players = 0
    for match in general:
        home_count = tb_home.objects.filter(match_ID=match.match_ID).count()
        away_count = tb_away.objects.filter(match_ID=match.match_ID).count()
        max_home_players = max(max_home_players, home_count)
        max_away_players = max(max_away_players, away_count)

    # Boş oyuncu şablonları
    empty_home_player = {
        "home_player_" + field: "-" for field in [
            "name", "shirt_number", "nation", "pos", "age", "min", 
            "gls", "ast", "pk", "pkatt", "sh", "sot", "crdy", "crdr",
            "touches", "tkl", "int", "blocks", "xg", "npxg", "xag",
            "sca", "gca", "cmp", "att", "cmp_rate", "prgp", "carries",
            "prgc", "att2", "succ"
        ]
    }
    
    empty_away_player = {
        "away_player_" + field: "-" for field in [
            "name", "shirt_number", "nation", "pos", "age", "min", 
            "gls", "ast", "pk", "pkatt", "sh", "sot", "crdy", "crdr",
            "touches", "tkl", "int", "blocks", "xg", "npxg", "xag",
            "sca", "gca", "cmp", "att", "cmp_rate", "prgp", "carries",
            "prgc", "att2", "succ"
        ]
    }

    merged_data = []
    for match in general:
        home_players = list(tb_home.objects.filter(match_ID=match.match_ID))
        away_players = list(tb_away.objects.filter(match_ID=match.match_ID))
        
        # Eksik oyuncular için boş kayıtlar ekle
        home_players.extend([empty_home_player.copy() for _ in range(max_home_players - len(home_players))])
        away_players.extend([empty_away_player.copy() for _ in range(max_away_players - len(away_players))])

        merged_data.append({
            "match": match,
            "home_players": home_players,
            "away_players": away_players,
        })

    context = {
        "leagues": data["leagues"],
        "seasons": data["seasons"],
        "merged_data": merged_data,
        "selected_league": selected_league_first if selected_league_first != "None" else None,
        "selected_season": selected_season if selected_season != "None" else None,
    }
    return render(request, "blog/collect_data.html", context)

def scrape_matches(selected_league, selected_season, formatted_date, match_id,request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    # genel_id = match_id
    league_id = league_data[selected_league]["id"]
    league_slug = league_data[selected_league]["slug"]
    base_url = f"https://fbref.com/en/comps/{league_id}/{selected_season}/schedule/{selected_season}-{league_slug}"
    driver.get(base_url)

    column_headers = ["id", "league", "season", "wk", "day", "date", "time","home","xg1","score","xg2","away","attendance","venue","referee"]
    match_found = False
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-row]")
        for row in rows:
            match_date_element = row.find_element(By.CSS_SELECTOR, '[data-stat="date"]')
            match_date_text = match_date_element.text.strip()
            try:
                row_date = datetime.datetime.strptime(match_date_text, "%Y-%m-%d")
            except ValueError:
                continue

            if row_date.date() == formatted_date.date():
                match_found = True
                row_data = [selected_league,selected_season]
                
                cells = row.find_elements(By.XPATH, ".//*[@class='right ' or @class='left ' or @class='center ' or @class='left sort_show' or @class='right sort_show' or @class='right iz']")
                for cell in cells:
                    cell_text = cell.text.strip()
                    if cell_text == "":  # Hücre boşsa
                        row_data.append("")
                    elif any(char.isdigit() for char in cell_text) and '.' in cell_text:
                        row_data.append(f'"{cell_text}"')  # Sayısal veri ise
                    else:
                        row_data.append(cell_text)  # Diğer veriler için
                if row_data:
                    row_data.pop()
                    if selected_league == "Super Lig":
                        row_data.insert(7,"")
                        row_data.insert(9,"")
                        match_data = [match_id] + row_data
                    elif selected_league == "Bundesliga" and int(selected_season.split('-')[0]) <= 2022:
                        row_data.pop(2)
                        match_data = [match_id] + row_data
                    else:
                        match_data = [match_id] + row_data
                    file_exists = os.path.isfile("data_general.csv")                    
                    with open("data_general.csv", mode="a", newline="", encoding="utf-8") as general_file:
                        writer = csv.writer(general_file)
                        if not file_exists:
                            writer.writerow(column_headers)
                        writer.writerow(match_data)  # Her satırı anında yaz         
                    print("Genel maç verileri yazıldı.")
                    # genel_id += 1
                # Detaylar için maç linkine tıkla
            #     match_link = row.find_element(By.CSS_SELECTOR, '[data-stat="match_report"] a').get_attribute("href")
            #     driver.get(match_link)
            #     time.sleep(2)

            #     # Takım istatistiklerini al
            #     tables = driver.find_elements(By.CSS_SELECTOR, ".stats_table.sortable.now_sortable")
            #     print(f"Bulunan tablo sayısı: {len(tables)}")

            #     # Ev sahibi istatistikleri
            #     home_table = tables[0]
            #     home_rows = home_table.find_elements(By.CSS_SELECTOR, "tr[data-row]")

            #     with open("data_home.csv", mode="w", newline="", encoding="utf-8") as home_file:
            #             writer = csv.writer(home_file)
            #             for row in home_rows[:len(home_rows)-1]:  # Başlık satırını atla
            #                 cells = row.find_elements(By.CSS_SELECTOR, "td, th")
            #                 row_data = []
            #                 for cell in cells:
            #                     cell_text = cell.text.strip()
            #                     if cell_text == "":  # Hücre boşsa
            #                         row_data.append("")
            #                     elif any(char.isdigit() for char in cell_text) and '.' in cell_text:
            #                         row_data.append(f'"{cell_text}"')  # Sayısal veri ise
            #                     else:
            #                         row_data.append(cell_text)
            #                 match_data = [match_id] + row_data  # Her oyuncu için ayrı satır
            #                 writer.writerow(match_data)
            # # Deplasman istatistikleri
            #     if len(tables) >= 8:
            #             away_team_table = tables[7]
            #             away_rows = away_team_table.find_elements(By.CSS_SELECTOR, "tr[data-row]")
            #             #away_players = []
            #             with open("data_away.csv", mode="w", newline="", encoding="utf-8") as away_file:
            #                 writer = csv.writer(away_file)
            #                 for row in away_rows[:len(home_rows)-1]:
            #                     cells = row.find_elements(By.CSS_SELECTOR, "td, th")  
            #                     row_data = []
            #                     for cell in cells:
            #                         cell_text = cell.text.strip()
            #                         if cell_text == "":  # Hücre boşsa
            #                             row_data.append("")
            #                         elif any(char.isdigit() for char in cell_text) and '.' in cell_text:
            #                             row_data.append(f'"{cell_text}"')  # Sayısal veri ise
            #                         else:
            #                             row_data.append(cell_text)
            #                     match_data = [match_id] + row_data  # Her oyuncu için ayrı satır
            #                     writer.writerow(match_data)
                
            #     elif len(tables) >= 4:
            #             away_team_table = tables[2]
            #             away_rows = away_team_table.find_elements(By.CSS_SELECTOR, "tr[data-row]")
            #             #away_players = []
            #             with open("data_away.csv", mode="w", newline="", encoding="utf-8") as away_file:
            #                 writer = csv.writer(away_file)
            #                 for row in away_rows[:len(home_rows)-1]:  
            #                     cells = row.find_elements(By.CSS_SELECTOR, "td, th")  
            #                     row_data = []
            #                     for cell in cells:
            #                         cell_text = cell.text.strip()
            #                         if cell_text == "":  # Hücre boşsa
            #                             row_data.append("")
            #                         elif any(char.isdigit() for char in cell_text) and '.' in cell_text:
            #                             row_data.append(f'"{cell_text}"')  # Sayısal veri ise
            #                         else:
            #                             row_data.append(cell_text)
            #                     match_data = [match_id] + row_data  # Her oyuncu için ayrı satır
            #                     writer.writerow(match_data)
            #     driver.back()
            #     driver.implicitly_wait(30)
                match_id += 1
        if not match_found:
            messages.warning(request, "Belirtilen tarihte maç oynanmamıştır.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

    driver.quit()
def read_csv_to_dict(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
def clear_csv_file(file_name):
    try:
        with open(file_name, mode="r", encoding="utf-8") as file:
            lines = file.readlines()  # Dosyadaki tüm satırları oku

        if lines:
            with open(file_name, mode="w", newline="", encoding="utf-8") as file:
                file.write(lines[0])  # İlk satırı yaz
                # Diğer satırları atla, yalnızca ilk satır kalır
        else:
            print("Dosya boş, işlem yapılmadı.")
    except FileNotFoundError:
        print(f"{file_name} dosyası bulunamadı.")
    except Exception as e:
        print(f"Hata oluştu: {e}")
# def merge_data(matches, home_players, away_players):
#     merged_data = []
#     for match in matches:
#         match_id = match['id']  # CSV'de eşleşme için ortak bir ID kullan
#         match_data = {
#             'match': match,
#             'home_players': [player for player in home_players if player['match_id'] == match_id],
#             'away_players': [player for player in away_players if player['match_id'] == match_id]
#         }
#         merged_data.append(match_data)
#     return merged_data    
def live_collect_data(request):
    form = DateField(request.GET)
    
    # Sadece form submit edildiğinde işlem yap
    if request.GET:
        selected_date = None
        selected_league = request.GET.get('league', '')
        selected_season = request.GET.get('season', '')
        
        if form.is_valid():
            selected_date = form.cleaned_data.get('match_date')
            
            try:
                formatted_date = datetime.datetime.strptime(str(selected_date), "%Y-%m-%d")
                
                # Veri çekme ve işleme işlemleri
                scrape_matches(selected_league, selected_season, formatted_date, 1, request)
                matches = read_csv_to_dict('data_general.csv')
                
                merged_data = []
                for match in matches:
                    match_data = {'match': match}
                    merged_data.append(match_data)
                    
                clear_csv_file("data_general.csv")
                
                context = {
                    "leagues": data_live["leagues"],
                    "seasons": data_live["seasons"],
                    "form": form,
                    "selected_league": selected_league,
                    "selected_season": selected_season,
                    "merged_data": merged_data,
                }
                
                return render(request, "blog/live_collect_data.html", context)
                
            except ValueError:
                pass  # Tarih format hatası - JavaScript zaten kontrol ediyor
    
    # İlk sayfa yüklemesi veya hatalı form durumu
    context = {
        "leagues": data_live["leagues"],
        "seasons": data_live["seasons"],
        "form": form,
    }
    
    return render(request, "blog/live_collect_data.html", context)
def predict(request):
    return render(request, "blog/predict.html")