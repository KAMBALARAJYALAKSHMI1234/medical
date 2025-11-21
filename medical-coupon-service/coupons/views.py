from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Plan, Coupon
from .serializers import PlanSerializer, CouponSerializer


# ---------------- PLAN CRUD ----------------

class PlanListCreateView(APIView):

    def get(self, request):
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Plan created", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=400)


class PlanDetailView(APIView):

    def get_object(self, pk):
        try:
            return Plan.objects.get(PLAN_ID=pk)
        except Plan.DoesNotExist:
            return None

    def get(self, request, pk):
        plan = self.get_object(pk)
        if not plan:
            return Response({"error": "Plan not found"}, status=404)
        serializer = PlanSerializer(plan)
        return Response(serializer.data)

    def put(self, request, pk):
        plan = self.get_object(pk)
        if not plan:
            return Response({"error": "Plan not found"}, status=404)

        serializer = PlanSerializer(plan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Plan updated", "data": serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        plan = self.get_object(pk)
        if not plan:
            return Response({"error": "Plan not found"}, status=404)
        plan.delete()
        return Response({"message": "Plan deleted"})


# ---------------- COUPON CRUD ----------------

class CouponListCreateView(APIView):

    def get(self, request):
        coupons = Coupon.objects.all()
        serializer = CouponSerializer(coupons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Coupon created", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=400)


class CouponDetailView(APIView):

    def get_object(self, pk):
        try:
            return Coupon.objects.get(COUPON_ID=pk)
        except Coupon.DoesNotExist:
            return None

    def get(self, request, pk):
        coupon = self.get_object(pk)
        if not coupon:
            return Response({"error": "Coupon not found"}, status=404)
        serializer = CouponSerializer(coupon)
        return Response(serializer.data)

    def put(self, request, pk):
        coupon = self.get_object(pk)
        if not coupon:
            return Response({"error": "Coupon not found"}, status=404)

        serializer = CouponSerializer(coupon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Coupon updated", "data": serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        coupon = self.get_object(pk)
        if not coupon:
            return Response({"error": "Coupon not found"}, status=404)
        coupon.delete()
        return Response({"message": "Coupon deleted"})
