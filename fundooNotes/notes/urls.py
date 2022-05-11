from django.urls import path
from notes import views

urlpatterns = [
    path('note', views.Notes.as_view(), name='note'),
    path('note/<int:pk>', views.NoteDelete.as_view(), name='note_delete')
]
