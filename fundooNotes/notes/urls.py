from django.urls import path
from notes import views

urlpatterns = [
    path('note', views.Notes.as_view(), name='note'),
    path('note/<int:pk>', views.Notes.as_view(), name='note_detail')
    # path('notes', views.note_list)
]
