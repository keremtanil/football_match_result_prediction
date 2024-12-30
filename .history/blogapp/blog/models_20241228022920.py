from django.db import models

class tb_general(models.Model):
    match_ID = models.BigAutoField
    wk = models.CharField(max_length=100)
    day = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    home = models.CharField(max_length=100)
    xg1 = models.CharField(max_length=100)
    score = models.CharField(max_length=100)
    xg2 = models.CharField(max_length=100)
    away = models.CharField(max_length=100)
    attendance = models.CharField(max_length=100)
    venue = models.CharField(max_length=200)
    referee = models.CharField(max_length=100)

    class Meta:
        db_table = 'tb_general'

class tb_home(models.Model):
    match_ID = models.BigAutoField
    home_player_name = models.CharField(max_length=100)
    home_player_shirt_number = models.CharField(max_length=100)
    home_player_nation = models.CharField(max_length=100)
    home_player_pos = models.CharField(max_length=100)
    home_player_age = models.CharField(max_length=100)
    home_player_min = models.CharField(max_length=100)
    home_player_gls = models.CharField(max_length=100)
    home_player_ast = models.CharField(max_length=100)
    home_player_pk = models.CharField(max_length=100)
    home_player_pkatt = models.CharField(max_length=100)
    home_player_sh = models.CharField(max_length=100)
    home_player_sot = models.CharField(max_length=100)
    home_player_crdy = models.CharField(max_length=100)
    home_player_crdr = models.CharField(max_length=100)
    home_player_touches = models.CharField(max_length=100)
    home_player_tkl = models.CharField(max_length=100)
    home_player_int = models.CharField(max_length=100)
    home_player_blocks = models.CharField(max_length=100)
    home_player_xg = models.CharField(max_length=100)
    home_player_npxg = models.CharField(max_length=100)
    home_player_xag = models.CharField(max_length=100)
    home_player_sca = models.CharField(max_length=100)
    home_player_gca = models.CharField(max_length=100)
    home_player_cmp = models.CharField(max_length=100)
    home_player_att = models.CharField(max_length=100)
    home_player_cmp_rate = models.CharField(max_length=100)
    home_player_prgp = models.CharField(max_length=100)
    home_player_carries = models.CharField(max_length=100)
    home_player_prgc = models.CharField(max_length=100)
    home_player_att2 = models.CharField(max_length=100)
    home_player_succ = models.CharField(max_length=100)

    class Meta:
        db_table = 'tb_home'

class tb_away(models.Model):
    match_ID = models.BigAutoField
    away_player_name = models.CharField(max_length=100)
    away_player_shirt_number = models.CharField(max_length=100)
    away_player_nation = models.CharField(max_length=100)
    away_player_pos = models.CharField(max_length=100)
    away_player_age = models.CharField(max_length=100)
    away_player_min = models.CharField(max_length=100)
    away_player_gls = models.CharField(max_length=100)
    away_player_ast = models.CharField(max_length=100)
    away_player_pk = models.CharField(max_length=100)
    away_player_pkatt = models.CharField(max_length=100)
    away_player_sh = models.CharField(max_length=100)
    away_player_sot = models.CharField(max_length=100)
    away_player_crdy = models.CharField(max_length=100)
    away_player_crdr = models.CharField(max_length=100)
    away_player_touches = models.CharField(max_length=100)
    away_player_tkl = models.CharField(max_length=100)
    away_player_int = models.CharField(max_length=100)
    away_player_blocks = models.CharField(max_length=100)
    away_player_xg = models.CharField(max_length=100)
    away_player_npxg = models.CharField(max_length=100)
    away_player_xag = models.CharField(max_length=100)
    away_player_sca = models.CharField(max_length=100)
    away_player_gca = models.CharField(max_length=100)
    away_player_cmp = models.CharField(max_length=100)
    away_player_att = models.CharField(max_length=100)
    away_player_cmp_rate = models.CharField(max_length=100)
    away_player_prgp = models.CharField(max_length=100)
    away_player_carries = models.CharField(max_length=100)
    away_player_prgc = models.CharField(max_length=100)
    away_player_att2 = models.CharField(max_length=100)
    away_player_succ = models.CharField(max_length=100)

    class Meta:
        db_table = 'tb_away'


