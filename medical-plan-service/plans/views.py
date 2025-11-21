# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .models import Plan
# from .serializers import PlanSerializer
# from django.shortcuts import get_object_or_404

# class PlanViewSet(viewsets.ModelViewSet):
#     queryset = Plan.objects.all()
#     serializer_class = PlanSerializer
#     lookup_field = "plan_id"
#     filterset_fields = ["is_active", "price"]
#     search_fields = ["plan_name"]
#     ordering_fields = ["price", "duration", "created_at"]

#     @action(detail=True, methods=["post"])
#     def activate(self, request, plan_id=None):
#         plan = get_object_or_404(Plan, plan_id=plan_id)
#         plan.is_active = True
#         plan.save(update_fields=["is_active", "updated_at"])
#         return Response({"detail": "Plan activated.", "plan_id": plan.plan_id}, status=status.HTTP_200_OK)

#     @action(detail=True, methods=["post"])
#     def deactivate(self, request, plan_id=None):
#         plan = get_object_or_404(Plan, plan_id=plan_id)
#         plan.is_active = False
#         plan.save(update_fields=["is_active", "updated_at"])
#         return Response({"detail": "Plan deactivated.", "plan_id": plan.plan_id}, status=status.HTTP_200_OK)

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import IntegrityError
import traceback
from .models import Plan
from .serializers import PlanSerializer

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)

        except IntegrityError as e:
            return Response(
                {"errors": "Database integrity error", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"errors": str(e), "traceback": traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
