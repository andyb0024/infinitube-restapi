from django.db import models
from InfinitubeApi.utils import unique_slug_generator
from django.db.models.signals import post_save,pre_save
from memberships.models import Membership
from django.urls import reverse
# Create your models here.
class Artiste(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Album(models.Model):

    title = models.CharField(max_length=120)
    artiste= models.ForeignKey(Artiste, related_name='album', on_delete=models.CASCADE, null=True)
    image= models.ImageField(default=False,null=True)
    allowed_memberships = models.ManyToManyField(Membership)
    def __str__(self):
        return self.title
    # def get_absolute_url(self):
    #     # return '/course/{slug}/'.format(slug=self.slug)
    #     return reverse('Videos:album-detail', kwargs={"pk": self.pk})
    #
    #     # return f'/courses/{self.slug}'
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    @property
    def musics(self):
        return self.music_set.all().order_by('position')

class Music(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    title = models.CharField(max_length=120)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    def __str__(self):
        return self.title
    # def get_absolute_url(self):
    #     # return '/lesson/{slug}/'.format(slug=self.slug)
    #     return reverse('Videos:music_detail',
    #                    kwargs={
    #                        "pk": self.album.pk,
    #                        "music_slug": self.slug
    #                    })
    #



def music_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect( music_pre_save_receiver, sender=Music)

