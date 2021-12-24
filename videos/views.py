from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from .models import Album, Music
from .serializers import AlbumSerializer, MusicSerializer
from memberships.models import Membership, UserMembership


class AlbumListApiView(ListAPIView):
    serializer_class = AlbumSerializer

    def get_queryset(self):
        qs = Album.objects.all()
        return qs


class AlbumDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExists():
            raise Http404

    def get(self, request, pk):
        qs = self.get_object(pk)
        serializer = AlbumSerializer(qs)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        qs = self.get_object(pk)
        serializer = AlbumSerializer(qs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        qs = self.get_object(pk)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MusicDetailApiView(APIView):
    def get(self, request, pk, music_slug, *args, **kwargs):
        album_qs = Album.objects.filter(pk=pk)
        if album_qs.exists():
            album = album_qs.first()
        music_qs = album.musics.filter(slug=music_slug)
        if music_qs.exists():
            music = music_qs.first()
        serializer = MusicSerializer(music)
        context = {
            'Music': serializer.data
        }
        return Response(context)


class MusicDetailApiView(APIView):
    def get(self, request, pk, music_slug, *args, **kwargs):
        album_qs = Album.objects.filter(pk=pk)
        if album_qs.exists():
            album = album_qs.first()
        music_qs = album.musics.filter(slug=music_slug)
        if music_qs.exists():
            music = music_qs.first()
        serializer = MusicSerializer(music)
        user_membership = UserMembership.objects.filter(user=request.user.id).first()
        user_membership_type = user_membership.membership.membership_type
        print(user_membership_type)
        album_allowed_mem_types = album.allowed_memberships.all()
        print()
        context = {
            'message': "upgrade membership"
        }
        if album_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            context = {
                'Music': serializer.data
            }

        return Response(context)
