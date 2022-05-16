from django.urls import path, re_path
from notes import views

urlpatterns = [
    path('note', views.Notes.as_view(), name='note'),
    path('note/<int:note_id>', views.Notes.as_view(), name='delete'),
    path('label', views.Labels.as_view(), name='label'),
    path('search', views.SearchAPI.as_view(), name='search'),
    path('share', views.CollaboratorAPI.as_view(), name='share')

]
