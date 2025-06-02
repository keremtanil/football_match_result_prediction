from django.test import TestCase, Client
from django.urls import reverse
from blog.models import tb_general, tb_home, tb_away

# --- Unit Tests ---
class ModelUnitTests(TestCase):

    def setUp(self):
        # Test modelleri için örnek veri
        tb_general.objects.create(match_ID=1,league='Premier League',season='2023-2024',wk='35',day='Saturday',date='2024-05-01',time='15:00',home='Team A',xg1='1.5',score='2-1',xg2='0.8',away='Team B',attendance='25000',venue='Stadium XYZ',referee='Referee Name')
    def test_model_string_representation(self):
        match = tb_general.objects.get(id=1)
        self.assertEqual(str(match), f"{match.home_team} vs {match.away_team} - {match.league} {match.season}")

# --- Integration Tests ---
class ViewIntegrationTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Örnek veriler
        tb_general.objects.create(match_ID=1,league='Premier League',season='2023-2024',wk='35',day='Saturday',date='2024-05-01',time='15:00',home='Team A',xg1='1.5',score='2-1',xg2='0.8',away='Team B',attendance='25000',venue='Stadium XYZ',referee='Referee Name'
        )
        tb_home.objects.create(id=1, some_field='value')  # Alanları kendi modeline göre değiştir
        tb_away.objects.create(id=1, some_field='value')

    def test_index_view_status_and_template(self):
        url = reverse('')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_collect_data_view_no_filter(self):
        url = reverse('collect_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('merged_data', response.context)
        self.assertTrue(len(response.context['merged_data']) > 0)

    def test_collect_data_view_with_filters(self):
        url = reverse('collect_data')
        response = self.client.get(url, {'league': 'Premier League', 'season': '2023-2024'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_league'], 'Premier League')
        self.assertEqual(response.context['selected_season'], '2023-2024')

# --- Functional Tests ---
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

class FunctionalTests(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()  # ChromeDriver yolunu ayarla ya da Firefox kullan
        tb_general.objects.create(match_ID=1,league='Premier League',season='2023-2024',wk='35',day='Saturday',date='2024-05-01',time='15:00',home='Team A',xg1='1.5',score='2-1',xg2='0.8',away='Team B',attendance='25000',venue='Stadium XYZ',referee='Referee Name')

    def tearDown(self):
        self.driver.quit()

    def test_homepage_loads_and_shows_match(self):
        self.driver.get(self.live_server_url + reverse(''))
        # Örnek: Ana sayfada "Premier League" yazısı görünür mü?
        body_text = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Premier League', body_text)

# --- Acceptance Tests ---
class AcceptanceTests(TestCase):

    def setUp(self):
        self.client = Client()
        tb_general.objects.create(match_ID=1,league='Premier League',season='2023-2024',wk='35',day='Saturday',date='2024-05-01',time='15:00',home='Team A',xg1='1.5',score='2-1',xg2='0.8',away='Team B',attendance='25000',venue='Stadium XYZ',referee='Referee Name')

    def test_user_can_filter_matches_by_league_and_season(self):
        url = reverse('collect_data')
        response = self.client.get(url, {'league': 'Premier League', 'season': '2023-2024'})
        self.assertEqual(response.status_code, 200)
        data = response.context['merged_data']
        # Tüm sonuçların filtrelere uygun olduğunu doğrula
        for item in data:
            self.assertEqual(item.league, 'Premier League')
            self.assertEqual(item.season, '2023-2024')


