# from rest_framework import serializers
# from .models import Doctor
# from django.utils import timezone
# from datetime import timedelta
# import re

# MOBILE_REGEX = re.compile(r'^\+?\d{6,15}$')  # basic international check

# class DoctorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Doctor
#         fields = "__all__"
#         read_only_fields = ("doctor_id", "created_at", "updated_at")

#     def validate_mobile(self, value):
#         if not MOBILE_REGEX.match(value):
#             raise serializers.ValidationError("Mobile must be digits, 6-15 chars, optional leading +.")
#         # Optionally enforce uniqueness:
#         qs = Doctor.objects.filter(mobile=value)
#         if self.instance:
#             qs = qs.exclude(pk=self.instance.pk)
#         if qs.exists():
#             raise serializers.ValidationError("This mobile number is already registered.")
#         return value

#     def validate_email(self, value):
#         qs = Doctor.objects.filter(email=value)
#         if self.instance:
#             qs = qs.exclude(pk=self.instance.pk)
#         if qs.exists():
#             raise serializers.ValidationError("This email is already registered.")
#         return value

#     def validate_otp(self, value):
#         # If OTP provided, ensure length and digits
#         if value is not None and value != "":
#             if not value.isdigit() or len(value) > 10:
#                 raise serializers.ValidationError("OTP must be numeric and up to 10 digits.")
#         return value

#     def validate(self, attrs):
#         # Example cross-field validation: if email_verified True, email must be present
#         if attrs.get("email_verified") and not (attrs.get("email") or (self.instance and self.instance.email)):
#             raise serializers.ValidationError({"email": "Email is required if email_verified is True."})
#         return attrs


from rest_framework import serializers
from .models import Doctor
from django.utils import timezone
from datetime import timedelta
import re

MOBILE_REGEX = re.compile(r'^\+?\d{6,15}$')  # basic international check

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = ("doctor_id", "created_at", "updated_at")

    def _to_bool_normalized(self, v):
        """
        Normalize many possible boolean representations to Python bool:
        - bytes / bytearray (e.g. b'\x00' / b'\x01')
        - string '0'/'1' or 'true'/'false'
        - integers 0/1
        - actual bool
        - None -> False
        """
        if v is None:
            return False
        # bytes from BIT(1)
        if isinstance(v, (bytes, bytearray)):
            try:
                return bool(int.from_bytes(v, byteorder="big"))
            except Exception:
                return v == b'\x01'
        # strings
        if isinstance(v, str):
            low = v.strip().lower()
            if low in ("true", "false"):
                return low == "true"
            if low.isdigit():
                return bool(int(low))
            # fallback: non-empty string -> True
            return bool(low)
        # numbers
        if isinstance(v, (int, float)):
            try:
                return bool(int(v))
            except Exception:
                return bool(v)
        # already bool or other truthy value
        return bool(v)

    def update(self, instance, validated_data):
        """
        Normalize boolean-like fields both from DB instance (in case they are bytes)
        and incoming validated_data before saving.
        """
        bool_fields = (
            "mobile_number_verified",
            "email_verified",
            "gbp_available",
            "is_active",
        )

        # Normalize current instance values if they came as bytes from DB
        for field in bool_fields:
            if hasattr(instance, field):
                cur = getattr(instance, field)
                if isinstance(cur, (bytes, bytearray)):
                    setattr(instance, field, self._to_bool_normalized(cur))

        # Normalize incoming payload values
        for key in list(validated_data.keys()):
            if key in bool_fields:
                validated_data[key] = self._to_bool_normalized(validated_data.get(key))

        return super().update(instance, validated_data)

    # -------------------------
    # Existing validators below
    # -------------------------
    def validate_mobile(self, value):
        if not MOBILE_REGEX.match(value):
            raise serializers.ValidationError("Mobile must be digits, 6-15 chars, optional leading +.")
        # Optionally enforce uniqueness:
        qs = Doctor.objects.filter(mobile=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This mobile number is already registered.")
        return value

    def validate_email(self, value):
        qs = Doctor.objects.filter(email=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_otp(self, value):
        # If OTP provided, ensure length and digits
        if value is not None and value != "":
            if not str(value).isdigit() or len(str(value)) > 10:
                raise serializers.ValidationError("OTP must be numeric and up to 10 digits.")
        return value

    def validate(self, attrs):
        # Example cross-field validation: if email_verified True, email must be present
        # Note: use normalized bool just in case client sent '1'/'0'
        email_verified = attrs.get("email_verified")
        if email_verified is not None:
            email_verified = self._to_bool_normalized(email_verified)

        if email_verified and not (attrs.get("email") or (self.instance and self.instance.email)):
            raise serializers.ValidationError({"email": "Email is required if email_verified is True."})
        return attrs
