from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

class DoctorViewSet(viewsets.ModelViewSet):
    """
    Provides: list, retrieve, create, update, partial_update, destroy
    Extra actions:
      - POST /doctors/{pk}/send_otp/   -> generate and save OTP (mock)
      - POST /doctors/{pk}/verify_otp/ -> verify OTP
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    lookup_field = "doctor_id"
    filterset_fields = ["city", "state", "is_active", "specialization"]
    search_fields = ["first_name", "last_name", "email", "mobile", "specialization"]
    ordering_fields = ["created_at", "updated_at", "professional_experience_years"]

    def create(self, request, *args, **kwargs):
        # Default create with serializer validation; catch exceptions for clearer errors
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["post"])
    def send_otp(self, request, doctor_id=None):
        """Generate a fake OTP and save with timestamp (for demonstration)."""
        doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
        import random
        otp = f"{random.randint(100000, 999999)}"
        doctor.otp = otp
        doctor.otp_generated_time = timezone.now()
        doctor.save(update_fields=["otp", "otp_generated_time"])
        # In production: send via SMS/email provider. Here we return OTP for testing.
        return Response({"doctor_id": doctor.doctor_id, "otp": otp, "message": "OTP generated (for testing)."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def verify_otp(self, request, doctor_id=None):
        doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
        provided = request.data.get("otp")
        if not provided:
            return Response({"detail": "OTP required in JSON body."}, status=status.HTTP_400_BAD_REQUEST)
        # expiry 10 minutes
        if not doctor.otp or not doctor.otp_generated_time:
            return Response({"detail": "No OTP generated for this doctor."}, status=status.HTTP_400_BAD_REQUEST)
        if timezone.now() > doctor.otp_generated_time + timedelta(minutes=10):
            return Response({"detail": "OTP expired."}, status=status.HTTP_400_BAD_REQUEST)
        if doctor.otp != str(provided):
            return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        doctor.mobile_number_verified = True
        doctor.otp = None
        doctor.otp_generated_time = None
        doctor.save(update_fields=["mobile_number_verified", "otp", "otp_generated_time"])
        return Response({"detail": "OTP verified.", "doctor_id": doctor.doctor_id}, status=status.HTTP_200_OK)

