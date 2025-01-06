from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import tb_general
from .models import tb_home
from .models import tb_away
@admin.register(tb_general)
class TbGeneralAdmin(admin.ModelAdmin):
    list_display = ('match_ID', )  # Görüntülenecek sütunları ekleyin

@admin.register(tb_home)
class TbHomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'match_ID', 'home_player_name')  # ForeignKey'i ve diğer alanları görüntüleyin
    list_filter = ('match_ID', )  # Filtreleme için kullanabilirsiniz
    search_fields = ('home_player_name', )  # Arama alanı ekleyebilirsiniz

@admin.register(tb_away)
class TbAwayAdmin(admin.ModelAdmin):
    list_display = ('id', 'match_ID', 'away_player_name')
    list_filter = ('match_ID', )
    search_fields = ('away_player_name', )

