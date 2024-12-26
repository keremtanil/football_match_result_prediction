from django.db import models

class tb_collect(models.Model):
    league = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
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
        db_table = 'tb_collect'
