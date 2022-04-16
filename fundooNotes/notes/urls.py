from django.urls import path,re_path
from notes import views

urlpatterns = [
    path('note', views.Notes.as_view(), name='note'),
    path('note/<int:note_id>', views.Notes.as_view(), name='delete'),
    # re_path(r'^note/(?P<note_id>[0-9]{3})/$', views.Notes.as_view(), name='delete')
    # path('orderid',views.getNoteOrder)
]
