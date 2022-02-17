from django.urls import path
from notes import views

urlpatterns = [
    path('note', views.Notes.as_view(), name='note'),
    # path('notes', views.note_list)
]
