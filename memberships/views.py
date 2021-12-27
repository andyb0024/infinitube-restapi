from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from .models import Membership, UserMembership, Subscription
from .serializers import MembershipSerializer
from rest_framework import generics


def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user.id)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None


def get_user_subscription(request):
    user_subscrition_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request)
    )
    if user_subscrition_qs.exists():
        user_subscrition = user_subscrition_qs.first()
        return user_subscrition
    return None


def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
        membership_type=membership_type
    )
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None


class MembershipSelectView(APIView):

    def get(self, request, format=None):
        qs = Membership.objects.all()
        serializer = MembershipSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # get membership id
        selected_membership_id = request.data.get('id')
        membership_obj = Membership.objects.get(id=selected_membership_id)
        # get user subscription and user membership
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)
        selected_membership_qs = Membership.objects.filter(
            id=selected_membership_id
        )
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()
            '''
            ==============
            validation
            =============
            '''
        serializer = MembershipSerializer(membership_obj)
        context = {
            "selected": serializer.data
        }
        if user_membership.membership == selected_membership or user_subscription is not None:
            context = {
                "message": "you have already membership. your\
                 next payment is due {}".format('get this value from stripe')
            }
            # assign session
        request.session['selected_membership_type'] = selected_membership.membership_type
        return Response(context)
