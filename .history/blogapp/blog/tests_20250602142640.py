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
        self.assertEqual(str(match), f"{match.home} vs {match.away} - {match.league} {match.season}")

# --- Integration Tests ---
class ViewIntegrationTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Örnek veriler
        tb_general.objects.create(match_ID=1,league='Premier League',season='2023-2024',wk='35',day='Saturday',date='2024-05-01',time='15:00',home='Team A',xg1='1.5',score='2-1',xg2='0.8',away='Team B',attendance='25000',venue='Stadium XYZ',referee='Referee Name'
        )
        match_instance = tb_general.objects.get(id=1)  # veya oluşturmak için: tb_general.objects.create(...)

        # tb_home için örnek kayıt oluştur
        tb_home.objects.create(match_ID=match_instance,home_player_name='John Doe',home_player_shirt_number='10',home_player_nation='USA',home_player_pos='FW',home_player_age='25',home_player_min='90',home_player_gls='1',home_player_ast='0',home_player_pk='0',home_player_pkatt='0',home_player_sh='3',home_player_sot='2',home_player_crdy='1',home_player_crdr='0',home_player_touches='45',
            home_player_tkl='2',home_player_int='1',home_player_blocks='0',home_player_xg='0.5',home_player_npxg='0.4',home_player_xag='0.2',home_player_sca='3',home_player_gca='1',home_player_cmp='30',home_player_att='35',home_player_cmp_rate='85.7',home_player_prgp='5',home_player_carries='20',home_player_prgc='4',home_player_att2='10',home_player_succ='7')

        # tb_away için örnek kayıt oluştur
        tb_away.objects.create(match_ID=match_instance,away_player_name='Jane Smith',away_player_shirt_number='8',away_player_nation='ENG',away_player_pos='MF',away_player_age='27',away_player_min='90',away_player_gls='0',away_player_ast='1',away_player_pk='0',away_player_pkatt='0',away_player_sh='2',away_player_sot='1',away_player_crdy='0',away_player_crdr='0',
            away_player_touches='60',away_player_tkl='3',away_player_int='2',away_player_blocks='1',away_player_xg='0.1',away_player_npxg='0.1',away_player_xag='0.4',away_player_sca='5',away_player_gca='1',away_player_cmp='50',away_player_att='55',away_player_cmp_rate='90.9',away_player_prgp='7',away_player_carries='25',away_player_prgc='6',away_player_att2='15',away_player_succ='10')

    def test_index_view_status_and_template(self):
        url = reverse('')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_collect_data_view_no_filter(self):
        url = reverse('collect')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('merged_data', response.context)
        self.assertTrue(len(response.context['merged_data']) > 0)

    def test_collect_data_view_with_filters(self):
        url = reverse('collect')
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
        url = reverse('collect')
        response = self.client.get(url, {'league': 'Premier League', 'season': '2023-2024'})
        self.assertEqual(response.status_code, 200)
        data = response.context['merged_data']
        # Tüm sonuçların filtrelere uygun olduğunu doğrula
        for item in data:
            self.assertEqual(item.league, 'Premier League')
            self.assertEqual(item.season, '2023-2024')


