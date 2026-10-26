from django.contrib import admin
from django.urls import path
from athletes_base import views as aviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', aviews.index, name='index'),
    path('add/', aviews.add_form, name='add_form'),
    path('upload/', aviews.upload_file, name='upload_file'),
    path('search/', aviews.search_db, name='search_db'),
    path('edit/<int:athlete_id>/', aviews.edit_form, name='edit_form'),
    path('delete/<int:athlete_id>/', aviews.delete_form, name='delete_form'),
]
