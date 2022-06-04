import views as views
from django.contrib import admin
from django.urls import path

from resource_api import views


urlpatterns = [
    path('Note/', views.NoteListApiView.as_view()),
    path('Note/<int:pk>', views.DetailAPIView.as_view()),
    path('Note/public', views.PublicNoteListAPIView.as_view()),
    path('About/', views.AboutTempLate.as_view()),
    path('Comment/', views.CommentListCreateAPIView.as_view()),
]
