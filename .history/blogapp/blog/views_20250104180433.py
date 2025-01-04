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
    "leagues":[
        {
            "league": "TUR-m",
        },
        {
            "league": "Premier League",
        },
        {
            "league": "GER-m",
        },
        {
            "league": "ITA-m",
        },
        {
            "league": "ESP-m",
        },
        {
            "league": "FRA-m",
        },
        {
            "league": "None",
        }
    ],
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
    # Dropdown seçimlerini al
    selected_league = request.GET.get('league', None)
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

    # genel_data = [] 
    # home_data = []
    # away_data = []
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
                    with open("data_general.csv", mode="a", newline="", encoding="utf-8") as general_file:
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

                with open("data_home.csv", mode="a", newline="", encoding="utf-8") as home_file:
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
                        with open("data_away.csv", mode="a", newline="", encoding="utf-8") as away_file:
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
                        with open("data_away.csv", mode="a", newline="", encoding="utf-8") as away_file:
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
def read_csv_without_headers(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader] 
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
    scrape_matches(selected_league, selected_season, formatted_date, 1)
    # CSV dosyalarını yükleme
    match_data = read_csv_without_headers("data_general.csv")
    home_players = read_csv_without_headers("data_home.csv")
    away_players = read_csv_without_headers("data_away.csv")
    print(match_data)
    print(home_players)
    print(away_players)
    # Eşleşen sütunları kontrol et (ID bazlı)
    # combined_data = []
    # for match in match_data:
    #     row = {f"Match_Col_{i}": value for i, value in enumerate(match)}  # Maç bilgileri

    #     # Ev sahibi futbolcuları ekle
    #     for player in home_players:
    #         if player[0] in match:  # ID eşleşmesini kontrol et
    #             row[f"Home_Player_{player[0]}"] = player[1]  # ID ve isim

    #     # Deplasman futbolcuları ekle
    #     for player in away_players:
    #         if player[0] in match:  # ID eşleşmesini kontrol et
    #             row[f"Away_Player_{player[0]}"] = player[1]  # ID ve isim

    #     combined_data.append(row)
    
    # Dinamik sütunları belirle
    # home_columns = [f"Home_Player_{player[0]}" for player in home_players]
    # away_columns = [f"Away_Player_{player[0]}" for player in away_players]
    # all_columns = [f"Match_Col_{i}" for i in range(len(match_data[0]))] + home_columns + away_columns

    context = {
        "leagues": data["leagues"],
        "seasons": data["seasons"],
        "form": form,
        # 'combined_data': combined_data,  # Tüm veri
        # 'home_columns': home_columns,  # Ev sahibi sütunlar
        # 'away_columns': away_columns,  # Deplasman sütunlar
    }

    return render(request, "blog/live_collect_data.html", context)
# def live_collect_data(request):
#     form = DateField(request.GET)  # Formu request.GET ile alıyoruz
#     selected_date = None 
#     if form.is_valid():
#         selected_date = form.cleaned_data.get('match_date')  # match_date alanını alın
#     else:
#         # Form geçersiz olduğunda bir hata mesajı verebilirsiniz
#         return render(request, "blog/live_collect_data.html", {
#             "leagues": data["leagues"],
#             "seasons": data["seasons"],
#             "form": form,
#             "error_message": "Geçerli bir tarih seçmelisiniz.",
#         })

#     selected_league = request.GET.get('league')
#     selected_season = request.GET.get('season')
#     if not selected_date or not selected_league or not selected_season:
#         return render(request, "blog/live_collect_data.html", {
#             "leagues": data["leagues"],
#             "seasons": data["seasons"],
#             "form": form,
#             "error_message": "Tüm alanları doldurmalısınız.",
#         })
#     try:
#         # Seçilen tarihi dönüştürme
#         formatted_date = datetime.datetime.strptime(str(selected_date), "%Y-%m-%d")
#     except ValueError as e:
#         return render(request, "blog/live_collect_data.html", {
#             "leagues": data["leagues"],
#             "seasons": data["seasons"],
#             "form": form,
#         })

#     driver_path = "/usr/local/bin/chromedriver"

#     service = ChromeService(executable_path=driver_path)
#     driver = webdriver.Chrome(service=service)
#     wait = WebDriverWait(driver, 10)
#     driver.maximize_window()

#     output_file_general = "data_general.csv"
#     output_file_home = "data_home.csv"
#     output_file_away = "data_away.csv"

#     def initialize_csv(file_path, headers):
#         """CSV dosyasını başlıklarla başlatır."""
#         with open(file_path, mode="w", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)
#             writer.writerow(headers)

#     # CSV dosyalarını başlat
#     initialize_csv(output_file_general, [])
#     initialize_csv(output_file_home, [])
#     initialize_csv(output_file_away, [])

#     match_id = 1

#     league_data = {
#         "Premier League": {"id": "9", "slug": "Premier-League-Scores-and-Fixtures"},
#         "Ligue 1": {"id": "13", "slug": "Ligue-1-Scores-and-Fixtures"},
#         "Bundesliga": {"id": "20", "slug": "Bundesliga-Scores-and-Fixtures"},
#         "Serie A": {"id": "11", "slug": "Serie-A-Scores-and-Fixtures"},
#         "La Liga": {"id": "12", "slug": "La-Liga-Scores-and-Fixtures"},
#         "Super Lig": {"id": "26", "slug": "Super-Lig-Scores-and-Fixtures"}
#     }

#     def scrape_matches():
#         global match_id
#         genel_id = match_id

#         league_id = league_data[selected_league]["id"]
#         league_slug = league_data[selected_league]["slug"]

#         base_url = f"https://fbref.com/en/comps/{league_id}/{season}/schedule/{season}-{league_slug}"
#         driver.get(base_url)

#         try:
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-row]")

#             for row in rows:
#                 match_date_element = row.find_element(By.CSS_SELECTOR, '[data-stat="date"]')
#                 match_date_text = match_date_element.text.strip()

#                 try:
#                     row_date = datetime.datetime.strptime(match_date_text, "%Y-%m-%d")
#                 except ValueError:
#                     continue

#                 if row_date.date() == formatted_date.date():
#                     row_data = [selected_league,selected_season]
                    
#                     cells = row.find_elements(By.XPATH, ".//*[@class='right ' or @class='left ' or @class='center ' or @class='left sort_show' or @class='right sort_show' or @class='right iz']")
#                     for cell in cells:
#                         cell_text = cell.text.strip()
#                         if cell_text == "":  # Hücre boşsa
#                             row_data.append("")
#                         elif any(char.isdigit() for char in cell_text) and '.' in cell_text:
#                             row_data.append(f'"{cell_text}"')  # Sayısal veri ise
#                         else:
#                             row_data.append(cell_text)  # Diğer veriler için
#                     if row_data:
#                         row_data.pop()
#                         match_data = [genel_id] + row_data
#                         with open(output_file_general, mode="a", newline="", encoding="utf-8") as general_file:
#                             writer = csv.writer(general_file)
#                             writer.writerow(match_data)  # Her satırı anında yaz         
#                         print("Genel maç verileri yazıldı.")
#                         genel_id += 1

#                     # Detaylar için maç linkine tıkla
#                     match_link = row.find_element(By.CSS_SELECTOR, '[data-stat="match_report"] a').get_attribute("href")
#                     driver.get(match_link)
#                     time.sleep(2)

#                     # Takım istatistiklerini al
#                     tables = driver.find_elements(By.CSS_SELECTOR, ".stats_table.sortable.now_sortable")
#                     print(f"Bulunan tablo sayısı: {len(tables)}")

#                     # Ev sahibi istatistikleri
#                     home_table = tables[0]
#                     home_rows = home_table.find_elements(By.CSS_SELECTOR, "tr[data-row]")
#                     with open(output_file_home, mode="a", newline="", encoding="utf-8") as home_file:
#                             writer = csv.writer(home_file)
#                             for row in home_rows[:len(home_rows)-1]:  # Başlık satırını atla
#                                 cells = row.find_elements(By.CSS_SELECTOR, "td, th")
#                                 row_data = []
#                                 for cell in cells:
#                                     cell_text = cell.text.strip()
#                                     if cell_text == "":  # Hücre boşsa
#                                         row_data.append("")
#                                     elif any(char.isdigit() for char in cell_text) and '.' in cell_text:
#                                         row_data.append(f'"{cell_text}"')  # Sayısal veri ise
#                                     else:
#                                         row_data.append(cell_text)
#                                 match_data = [match_id] + row_data  # Her oyuncu için ayrı satır
#                                 writer.writerow(match_data)

                        
#                     print("Ev sahibi takım istatistikleri yazıldı.")
#                     # Deplasman istatistikleri
#                     if len(tables) >= 8:
#                             away_team_table = tables[7]
#                             away_rows = away_team_table.find_elements(By.CSS_SELECTOR, "tr[data-row]")
#                             #away_players = []
#                             with open(output_file_away, mode="a", newline="", encoding="utf-8") as away_file:
#                                 writer = csv.writer(away_file)
#                                 for row in away_rows[:len(home_rows)-1]:
#                                     cells = row.find_elements(By.CSS_SELECTOR, "td, th")  
#                                     row_data = []
#                                     for cell in cells:
#                                         cell_text = cell.text.strip()
#                                         if cell_text == "":  # Hücre boşsa
#                                             row_data.append("")
#                                         elif any(char.isdigit() for char in cell_text) and '.' in cell_text:
#                                             row_data.append(f'"{cell_text}"')  # Sayısal veri ise
#                                         else:
#                                             row_data.append(cell_text)
#                                     match_data = [match_id] + row_data  # Her oyuncu için ayrı satır
#                                     writer.writerow(match_data)

#                             print("Deplasman takım istatistikleri yazıldı.")
                    
#                     elif len(tables) >= 4:
#                             away_team_table = tables[2]
#                             away_rows = away_team_table.find_elements(By.CSS_SELECTOR, "tr[data-row]")
#                             #away_players = []
#                             with open(output_file_away, mode="a", newline="", encoding="utf-8") as away_file:
#                                 writer = csv.writer(away_file)
#                                 for row in away_rows[:len(home_rows)-1]:  
#                                     cells = row.find_elements(By.CSS_SELECTOR, "td, th")  
#                                     row_data = []
#                                     for cell in cells:
#                                         cell_text = cell.text.strip()
#                                         if cell_text == "":  # Hücre boşsa
#                                             row_data.append("")
#                                         elif any(char.isdigit() for char in cell_text) and '.' in cell_text:
#                                             row_data.append(f'"{cell_text}"')  # Sayısal veri ise
#                                         else:
#                                             row_data.append(cell_text)
#                                     match_data = [match_id] + row_data  # Her oyuncu için ayrı satır
#                                     writer.writerow(match_data)
#                     driver.back()
#                     time.sleep(2)
#                     match_id += 1

#         except Exception as e:
#             print(f"Hata oluştu: {e}")

#         driver.quit()

#     scrape_matches()

#     context = {
#         "leagues": data["leagues"],
#         "seasons": data["seasons"],
#         "form": form,
#     }
#     return render(request, "blog/live_collect_data.html", context)
def predict(request):
    return render(request, "blog/predict.html")