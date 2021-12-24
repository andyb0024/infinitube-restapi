from django.urls import path
from .views import AlbumListApiView, AlbumDetailApiView, MusicDetailApiView

urlpatterns = [
    path('album/', AlbumListApiView.as_view(), name='list'),
    path('album/<int:pk>/', AlbumDetailApiView.as_view(), name='album-detail-api'),
    path('album/<int:pk>/<music_slug>', MusicDetailApiView.as_view(), name='lesson_detail')

]
