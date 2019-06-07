from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url('^$', views.home, name='home'),
    url(r'^upload_csv/$', views.upload_csv, name='upload_csv'),
    url(r'^search/$', views.get_search_results, name='get_search_results'),
    url(r'^delete_records/$', views.delete_records, name='delete_records'),
]
