from django.contrib import admin
from .models import BirdSpecies, BirdRecord, Airport, ImportLog

@admin.register(BirdSpecies)
class BirdSpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'danger_level')
    search_fields = ('name',)

@admin.register(BirdRecord)
class BirdRecordAdmin(admin.ModelAdmin):
    list_display = ('species', 'quantity', 'location', 'risk_level', 'record_time')
    list_filter = ('risk_level', 'species', 'record_time')
    search_fields = ('location', 'species__name')
    readonly_fields = ('latitude', 'longitude')

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'ident', 'airport_type', 'iso_country', 'municipality')
    list_filter = ('airport_type', 'iso_country')
    search_fields = ('name', 'ident', 'municipality')
    readonly_fields = ('latitude', 'longitude')

@admin.register(ImportLog)
class ImportLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'log_type', 'file_name', 'status', 'success_count', 'error_count')
    list_filter = ('log_type', 'status', 'created_at')
    search_fields = ('file_name',)
    readonly_fields = ('details', 'error_messages', 'completed_at')
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        # 不允许手动添加日志，只能通过导入过程创建
        return False

    def has_change_permission(self, request, obj=None):
        # 不允许修改日志，只能查看
        return False

