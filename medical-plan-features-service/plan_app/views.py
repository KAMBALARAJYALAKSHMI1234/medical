from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PlanFeatures
from .serializers import PlanFeaturesSerializer


# CREATE
class PlanFeaturesCreate(APIView):
    def post(self, request):
        serializer = PlanFeaturesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# READ ALL
class PlanFeaturesList(APIView):
    def get(self, request):
        data = list(PlanFeatures.objects.values())
        return Response(data)


# READ ONE
class PlanFeaturesDetail(APIView):
    def get(self, request, pk):
        feature = get_object_or_404(PlanFeatures, pk=pk)
        serializer = PlanFeaturesSerializer(feature)
        return Response(serializer.data)


# UPDATE
class PlanFeaturesUpdate(APIView):
    def put(self, request, pk):
        feature = get_object_or_404(PlanFeatures, pk=pk)
        serializer = PlanFeaturesSerializer(feature, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE
class PlanFeaturesDelete(APIView):
    def delete(self, request, pk):
        feature = get_object_or_404(PlanFeatures, pk=pk)
        feature.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)
