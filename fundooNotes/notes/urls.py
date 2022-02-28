from django.urls import path
from . import views

urlpatterns = [
    path('note', views.NoteList.as_view(), name='note'),
    path('note/<int:id>', views.NotesDetails.as_view(), name='notes'),
]
