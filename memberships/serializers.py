from rest_framework import serializers

from memberships.models import Membership

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model=Membership
        fields=['membership_type']