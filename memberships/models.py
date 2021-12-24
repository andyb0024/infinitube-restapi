from django.db import models
from django.db.models.signals import post_save,pre_save
from accounts.models import User
from .utils import unique_slug_generator
import stripe
from InfinitubeApi.settings import STRIPE_PUB_KEY
# Create your models here.

MEMBERSHIP_CHOCES=(
    ('Medium','med'),
    ('Premium','pre'),
    ('Free','free')
)
class Membership(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    membership_type=models.CharField(choices=MEMBERSHIP_CHOCES,max_length=30,default='Free')
    price = models.DecimalField(decimal_places=2, max_digits=20)
    stripe_plan_id=models.CharField( max_length=40)

    def __str__(self):
        return self.membership_type



class UserMembership(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    membership=models.ForeignKey(Membership,related_name="membership",on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.user.username

class Subscription (models.Model):
    user_membership=models.ForeignKey(UserMembership,on_delete=models.CASCADE)
    stripe_subscription_id =models.CharField(max_length=40)
    active=models.BooleanField(default=True)

    def __str__(self):
        return  self.user_membership.user.username


def membership_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect( membership_pre_save_receiver, sender=Membership)

def post_user_membership_create(sender,instance,created,*args,**kwargs):
    if created:
        UserMembership.objects.get_or_create(user=instance)
    user_membership,created=UserMembership.objects.get_or_create(user=instance)
    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id =="":
        stripe.api_key=STRIPE_PUB_KEY
        new_customer_id=stripe.Customer.create(email=instance.email)
        user_membership.stripe_customer_id=new_customer_id['id']
        user_membership.save()
post_save.connect(post_user_membership_create,sender=User)