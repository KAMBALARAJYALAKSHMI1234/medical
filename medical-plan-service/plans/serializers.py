# plans/serializers.py
from rest_framework import serializers
from .models import Plan

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"

    def _to_bool_normalized(self, v):
        # Accept bytes, bytearray, '0'/'1' strings, ints, bools
        if isinstance(v, (bytes, bytearray)):
            try:
                return bool(int.from_bytes(v, byteorder="big"))
            except Exception:
                return v == b'\x01'
        if isinstance(v, str) and v.isdigit():
            return bool(int(v))
        return bool(v)

    def update(self, instance, validated_data):
        # normalize instance value (comes from DB) if it's bytes
        if hasattr(instance, "is_active"):
            cur = getattr(instance, "is_active")
            if isinstance(cur, (bytes, bytearray)):
                setattr(instance, "is_active", self._to_bool_normalized(cur))

        # normalize incoming value if present in payload
        if "is_active" in validated_data:
            validated_data["is_active"] = self._to_bool_normalized(validated_data["is_active"])

        return super().update(instance, validated_data)

    def validate_price(self, value):
        if int(value) <= 0:
            raise serializers.ValidationError("Price must be positive.")
        return int(value)

    def validate_duration(self, value):
        if int(value) <= 0:
            raise serializers.ValidationError("Duration must be positive.")
        return int(value)
