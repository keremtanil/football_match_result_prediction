from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import tb_general
from .models import tb_home
from .models import tb_away

@admin.register(tb_general)
class anyname(ImportExportModelAdmin):
        pass
admin.register(tb_general)
admin.site.register(tb_home)
admin.site.register(tb_away)
