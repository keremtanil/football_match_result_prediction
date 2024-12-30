from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import tb_general
from .models import tb_home
from .models import tb_away

from django.contrib import admin
from .models import TbGeneral, TbHome, TbAway

@admin.register(TbGeneral)
class TbGeneralAdmin(admin.ModelAdmin):
    list_display = ('match_ID', )  # Görüntülenecek sütunları ekleyin

@admin.register(TbHome)
class TbHomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'match_ID', 'player_name')  # ForeignKey'i ve diğer alanları görüntüleyin
    list_filter = ('match_ID', )  # Filtreleme için kullanabilirsiniz
    search_fields = ('player_name', )  # Arama alanı ekleyebilirsiniz

@admin.register(TbAway)
class TbAwayAdmin(admin.ModelAdmin):
    list_display = ('id', 'match_ID', 'player_name')
    list_filter = ('match_ID', )
    search_fields = ('player_name', )

