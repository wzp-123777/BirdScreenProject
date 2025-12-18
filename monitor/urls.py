from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_final, name='map_final'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('list/', views.record_list, name='record_list'),
    path('add/', views.add_record, name='add_record'),
    path('import-xls/', views.import_xls_view, name='import_xls'),
    path('logs/', views.logs_view, name='logs'),
    path('import-log/<int:log_id>/', views.import_log_detail_view, name='import_log_detail'),
    path('realtime-log/<int:log_id>/', views.realtime_log_view, name='realtime_log'),
    path('api/log-stream/<int:log_id>/', views.api_log_stream, name='log_stream_api'),
    path('api/project-log-stream/', views.project_log_stream, name='project_log_stream'),
    path('api/data/', views.api_dashboard_data, name='api_dashboard_data'),
    path('api/bird-records/', views.api_bird_records, name='bird_records_api'),
    path('api/airports/', views.api_airports, name='airports_api'),
    path('api/airports-full/', views.api_airports_full, name='airports_full_api'),
]