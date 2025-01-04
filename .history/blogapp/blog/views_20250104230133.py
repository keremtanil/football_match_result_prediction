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

data ={
    "leagues":[{"league": "Super Lig",},{"league": "Premier League",},{"league": "Bundesliga",},{"league": "Serie A",},{"league": "La Liga",},{"league": "Ligue 1",},{"league": "None",}],
    "seasons": [{"season": f"{year}-{year+1}"} for year in range(datetime.datetime.now().year -1, 2016, -1)] + [{"season": "None"}],
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
    # Dropdown seçimlerini al
    selected_league_first = request.GET.get('league', None)
    selected_league = league[selected_league_first]
    selected_season = request.GET.get('season', None)

    general = tb_general.objects.all()

    # Filtre uygula (dropdown seçimlerine göre)
    if selected_league and selected_league != "None":
        general = general.filter(league=selected_league)  # Eğer "league" modelde varsa

    if selected_season and selected_season != "None":
        season_year = selected_season.split('/')[0]
        general = general.filter(season=season_year)

    # Dinamik olarak oyuncu bilgilerini getirin
    merged_data = []
    for match in general:
        home_players = tb_home.objects.filter(match_ID=match.match_ID)
        away_players = tb_away.objects.filter(match_ID=match.match_ID)

        merged_data.append({
            "match": match,
            "home_players": list(home_players),
            "away_players": list(away_players),
        })
    context = {
        "leagues": data["leagues"],
        "seasons": data["seasons"],
        "merged_data": merged_data,
        "selected_league": selected_league if selected_league != "None" else None,
        "selected_season": selected_season if selected_season != "None" else None,
    }
    return render(request, "blog/collect_data.html", context)

def scrape_matches(selected_league, selected_season, formatted_date, match_id):
    driver = webdriver.Chrome()
    driver.maximize_window()
    genel_id = match_id
    league_id = league_data[selected_league]["id"]
    league_slug = league_data[selected_league]["slug"]
    base_url = f"https://fbref.com/en/comps/{league_id}/{selected_season}/schedule/{selected_season}-{league_slug}"
    driver.get(base_url)

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
                    match_data = [match_id] + row_data
                    with open("data_general.csv", mode="w", newline="", encoding="utf-8") as general_file:
                        writer = csv.writer(general_file)
                        writer.writerow(match_data)  # Her satırı anında yaz         
                    print("Genel maç verileri yazıldı.")
                    genel_id += 1
                # Detaylar için maç linkine tıkla
                match_link = row.find_element(By.CSS_SELECTOR, '[data-stat="match_report"] a').get_attribute("href")
                driver.get(match_link)
                time.sleep(2)

                # Takım istatistiklerini al
                tables = driver.find_elements(By.CSS_SELECTOR, ".stats_table.sortable.now_sortable")
                print(f"Bulunan tablo sayısı: {len(tables)}")

                # Ev sahibi istatistikleri
                home_table = tables[0]
                home_rows = home_table.find_elements(By.CSS_SELECTOR, "tr[data-row]")

                with open("data_home.csv", mode="w", newline="", encoding="utf-8") as home_file:
                        writer = csv.writer(home_file)
                        for row in home_rows[:len(home_rows)-1]:  # Başlık satırını atla
                            cells = row.find_elements(By.CSS_SELECTOR, "td, th")
                            row_data = []
                            for cell in cells:
                                cell_text = cell.text.strip()
                                if cell_text == "":  # Hücre boşsa
                                    row_data.append("")
                                elif any(char.isdigit() for char in cell_text) and '.' in cell_text:
                                    row_data.append(f'"{cell_text}"')  # Sayısal veri ise
                                else:
                                    row_data.append(cell_text)
                            match_data = [match_id] + row_data  # Her oyuncu için ayrı satır
                            writer.writerow(match_data)
            # Deplasman istatistikleri
                if len(tables) >= 8:
                        away_team_table = tables[7]
                        away_rows = away_team_table.find_elements(By.CSS_SELECTOR, "tr[data-row]")
                        #away_players = []
                        with open("data_away.csv", mode="w", newline="", encoding="utf-8") as away_file:
                            writer = csv.writer(away_file)
                            for row in away_rows[:len(home_rows)-1]:
                                cells = row.find_elements(By.CSS_SELECTOR, "td, th")  
                                row_data = []
                                for cell in cells:
                                    cell_text = cell.text.strip()
                                    if cell_text == "":  # Hücre boşsa
                                        row_data.append("")
                                    elif any(char.isdigit() for char in cell_text) and '.' in cell_text:
                                        row_data.append(f'"{cell_text}"')  # Sayısal veri ise
                                    else:
                                        row_data.append(cell_text)
                                match_data = [match_id] + row_data  # Her oyuncu için ayrı satır
                                writer.writerow(match_data)
                
                elif len(tables) >= 4:
                        away_team_table = tables[2]
                        away_rows = away_team_table.find_elements(By.CSS_SELECTOR, "tr[data-row]")
                        #away_players = []
                        with open("data_away.csv", mode="w", newline="", encoding="utf-8") as away_file:
                            writer = csv.writer(away_file)
                            for row in away_rows[:len(home_rows)-1]:  
                                cells = row.find_elements(By.CSS_SELECTOR, "td, th")  
                                row_data = []
                                for cell in cells:
                                    cell_text = cell.text.strip()
                                    if cell_text == "":  # Hücre boşsa
                                        row_data.append("")
                                    elif any(char.isdigit() for char in cell_text) and '.' in cell_text:
                                        row_data.append(f'"{cell_text}"')  # Sayısal veri ise
                                    else:
                                        row_data.append(cell_text)
                                match_data = [match_id] + row_data  # Her oyuncu için ayrı satır
                                writer.writerow(match_data)
            driver.back()
            time.sleep(2)
            match_id += 1

    except Exception as e:
        print(f"Hata oluştu: {e}")

    driver.quit()
def read_csv_to_dict(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
def merge_data(matches, home_players, away_players):
    merged_data = []
    for match in matches:
        match_id = match['id']  # CSV'de eşleşme için ortak bir ID kullan
        match_data = {
            'match': match,
            'home_players': [player for player in home_players if player['match_id'] == match_id],
            'away_players': [player for player in away_players if player['match_id'] == match_id]
        }
        merged_data.append(match_data)
    return merged_data    
def live_collect_data(request):
    form = DateField(request.GET)  # Formu request.GET ile alıyoruz
    selected_date = None 
    if form.is_valid():
        selected_date = form.cleaned_data.get('match_date')  # match_date alanını alın
    else:
        # Form geçersiz olduğunda bir hata mesajı verebilirsiniz
        return render(request, "blog/live_collect_data.html", {
            "leagues": data["leagues"],
            "seasons": data["seasons"],
            "form": form,
            "error_message": "Geçerli bir tarih seçmelisiniz.",
        })

    selected_league = request.GET.get('league')
    selected_season = request.GET.get('season')
    if not selected_date or not selected_league or not selected_season:
        return render(request, "blog/live_collect_data.html", {
            "leagues": data["leagues"],
            "seasons": data["seasons"],
            "form": form,
            "error_message": "Tüm alanları doldurmalısınız.",
        })
    try:
        # Seçilen tarihi dönüştürme
        formatted_date = datetime.datetime.strptime(str(selected_date), "%Y-%m-%d")
    except ValueError as e:
        return render(request, "blog/live_collect_data.html", {
            "leagues": data["leagues"],
            "seasons": data["seasons"],
            "form": form,
        })
    
    matches = read_csv_to_dict('data_general.csv')  # Match bilgilerini tutan CSV dosyası
    home_players = read_csv_to_dict('data_home.csv')  # Home oyuncularını tutan CSV dosyası
    away_players = read_csv_to_dict('data_away.csv')  # Away oyuncularını tutan CSV dosyası

    merged_data = merge_data(matches, home_players, away_players)

    context = {
        "leagues": data["leagues"],
        "seasons": data["seasons"],
        "form": form,
        'merged_data': merged_data,  # Tüm veri
    }

    return render(request, "blog/live_collect_data.html", context)
def predict(request):
    return render(request, "blog/predict.html")