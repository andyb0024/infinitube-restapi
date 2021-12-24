from rest_framework import serializers
from .models import Album, Artiste, Music


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artiste
        fields = ['name']


class MusicSerializer(serializers.ModelSerializer):
    artiste = ArtistSerializer(read_only=True)

    class Meta:
        model = Music
        fields = ['title', 'artiste']


class AlbumSerializer(serializers.ModelSerializer):
    artiste = ArtistSerializer()
    musics = MusicSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['title', 'artiste', 'get_image', 'musics']
