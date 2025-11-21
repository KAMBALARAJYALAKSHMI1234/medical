from rest_framework import serializers
from .models import Subscription
from django.db import models

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        extra_kwargs = {
            'coupon_id': {'required': False, 'allow_null': True}
        }
    
    def validate(self, data):
        doctor_id = data.get('doctor_id')
        plan_id = data.get('plan_id')
        is_active = data.get('is_active', False)
        
        # Only check for duplicates if creating an ACTIVE subscription
        if is_active:
            # Build the lookup filter
            lookup_filter = models.Q(
                doctor_id=doctor_id,
                plan_id=plan_id,
                is_active=True
            )
            
            # If updating an existing subscription, exclude it from the check
            if self.instance:
                lookup_filter &= ~models.Q(subscription_id=self.instance.subscription_id)
            
            # Check if duplicate active subscription exists
            if Subscription.objects.filter(lookup_filter).exists():
                raise serializers.ValidationError({
                    "error": "Doctor already has an active subscription for this plan. Please deactivate the existing subscription first."
                })
        
        return data