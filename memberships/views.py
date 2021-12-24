from rest_framework.generics import ListAPIView
from  rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from.models import Membership
from.serializers import MembershipSerializer



class MembershipSelectView(ListAPIView):
    serializer_class = MembershipSerializer
    def get_queryset(self):
        qs=Membership.objects.all()
        return qs