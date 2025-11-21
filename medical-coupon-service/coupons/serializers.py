from rest_framework import serializers
from .models import Coupon, Plan

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    PLAN_ID = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all()
    )

    class Meta:
        model = Coupon
        fields = "__all__"
