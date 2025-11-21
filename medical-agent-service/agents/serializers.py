# agents/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import Agent

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = [
            'agent_id','name','designation','mobileno','email','password',
            'remarks','is_active','created_at','updated_at','is_admin'
        ]
        read_only_fields = ['agent_id','created_at','updated_at']

    def create(self, validated_data):
        # Ensure DB-required timestamps are set
        now = timezone.now()
        validated_data.setdefault('created_at', now)
        validated_data.setdefault('updated_at', now)

        # Cast bit/boolean values properly
        if 'is_active' in validated_data:
            validated_data['is_active'] = bool(validated_data['is_active'])
        if 'is_admin' in validated_data:
            validated_data['is_admin'] = bool(validated_data['is_admin'])

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Always refresh updated_at on update
        validated_data['updated_at'] = timezone.now()
        return super().update(instance, validated_data)
