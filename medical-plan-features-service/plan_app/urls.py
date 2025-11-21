from django.urls import path
from .views import (
    PlanFeaturesCreate,
    PlanFeaturesList,
    PlanFeaturesDetail,
    PlanFeaturesUpdate,
    PlanFeaturesDelete,
)

urlpatterns = [
    path('plan-features/', PlanFeaturesList.as_view()),
    path('plan-features/create/', PlanFeaturesCreate.as_view()),
    path('plan-features/<int:pk>/', PlanFeaturesDetail.as_view()),
    path('plan-features/update/<int:pk>/', PlanFeaturesUpdate.as_view()),
    path('plan-features/delete/<int:pk>/', PlanFeaturesDelete.as_view()),
]
