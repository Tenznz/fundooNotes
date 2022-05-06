from django.urls import path
from notes import views

urlpatterns = [
    path('note', views.Notes.as_view(), name='note'),
    path('note/<int:id>', views.Notes.as_view(), name='gd_note')
]
