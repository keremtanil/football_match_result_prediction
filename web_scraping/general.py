import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver_path = "/usr/local/bin/chromedriver"
main_url = "https://fbref.com/en/"

service = ChromeService(executable_path=driver_path)
driver = webdriver.Chrome(service=service)
driver.get(main_url)

wait = WebDriverWait(driver, 10)
driver.maximize_window()

# CSV dosyası oluştur ve başlıkları yaz
output_file = "home_data.csv"
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([])# Başlık satırı

output_file_1 = "away_data.csv"
with open(output_file_1, mode="w", newline="", encoding="utf-8") as file_1:
    writer = csv.writer(file_1)
    writer.writerow([])

output_file_2 = "gm_data.csv"
with open(output_file_2, mode="w", newline="", encoding="utf-8") as file_2:
    writer = csv.writer(file_2)
    writer.writerow([])

match_id = 1

def scraping(league):
    global match_id
    genel_id = match_id
    driver.get("https://fbref.com/en/")
    # Dropdown'u tıkla
    click_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sr_fb_fave")))   
    driver.execute_script("arguments[0].scrollIntoView(true);", click_dropdown)
    time.sleep(2) 
    click_dropdown.click()
    
    # Ligi seç
    time.sleep(2)
    league_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"option[value='{league}']")))
    league_option.click()

    # "Complete Schedule and Results" butonuna tıkla
    time.sleep(2)
    select_results = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fave > div > div:nth-child(3) > div > div > a")))
    select_results.click()

    initial_year_info = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#meta > div:nth-child(2) > h1")))
    initial_year = int(initial_year_info.text.split("-")[0])
    print(initial_year)

    try:
        while initial_year >= 2018:
            # "Previous season" butonuna tıkla
            prev_season_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#meta > div:nth-child(2) > div > a.button2.prev")))
            driver.execute_script("arguments[0].click();", prev_season_button)
            time.sleep(3)
            
            initial_year_info = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#meta > div:nth-child(2) > h1")))
            initial_year = int(initial_year_info.text.split("-")[0])
            print(initial_year)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-row]")
                
            for row in rows[:1]:
                row_data = []
                #row_data.append(league)
                #row_data.append(initial_year)
                
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
                    match_data = [genel_id] + row_data
                    with open(output_file_2, mode="a", newline="", encoding="utf-8") as file_2:
                        writer = csv.writer(file_2)
                        writer.writerow(match_data)  # Her satırı anında yaz         
                    print("mac verileri yazdirildi.")
                    genel_id += 1

            # Sayfayı aşağı kaydır ve match_report elementlerini bul
            elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-stat="match_report"] a')))
            for index, element in enumerate(elements[:1], start=1):  # İlk maçı al
                try:
                    print(f"{index}. elemente tıklanıyor...")
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                    time.sleep(1)  # Kaydırma sonrası kısa bir bekleme
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(3)  # Tıklama sonrası bekleme

                    #league_info = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content > div:nth-child(2) > a"))).text.strip()
                    
                    tables = driver.find_elements(By.CSS_SELECTOR, ".stats_table.sortable.now_sortable")
                    print(f"Bulunan tablo sayısı: {len(tables)}")
                    # Tablo 1 (Ev sahibi) içeriklerini al
                    home_team_table = tables[0]
                    home_rows = home_team_table.find_elements(By.CSS_SELECTOR, "tr[data-row]")
                        
                    with open(output_file, mode="a", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
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

                    if len(tables) >= 8:
                        print("Tablolar başarıyla alındı!")
                        
                        away_team_table = tables[7]
                        away_rows = away_team_table.find_elements(By.CSS_SELECTOR, "tr[data-row]")
                        #away_players = []
                        with open(output_file_1, mode="a", newline="", encoding="utf-8") as file_1:
                            writer = csv.writer(file_1)
                            for row in away_rows[:len(home_rows)-1]:
                                cells = row.find_elements(By.CSS_SELECTOR, "td, th")  # Başlık satırını atla ve ilk 11 oyuncuyu al
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

                        print("Ev sahibi takım istatistikleri yazıldı.")

                    elif len(tables) >= 4:
                        print("Tablolar başarıyla alındı!")
                        
                        away_team_table = tables[2]
                        away_rows = away_team_table.find_elements(By.CSS_SELECTOR, "tr[data-row]")
                        #away_players = []
                        with open(output_file_1, mode="a", newline="", encoding="utf-8") as file_1:
                            writer = csv.writer(file_1)
                            for row in away_rows[:len(home_rows)-1]:  # Başlık satırını atla ve ilk 11 oyuncuyu al
                                cells = row.find_elements(By.CSS_SELECTOR, "td, th")  # Başlık satırını atla ve ilk 11 oyuncuyu al
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

                        print("Ev sahibi takım istatistikleri yazıldı.")
                    else:
                        print("Yeterli sayıda tablo bulunamadı.")

                    driver.back()  # Geri dön
                    time.sleep(2)  # Sayfa yüklenmesini bekle

                    match_id += 1

                except Exception as e:
                    print(f"{index}. elemente tıklanırken hata oluştu: {e}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

scraping("ENG-m")
driver.quit()