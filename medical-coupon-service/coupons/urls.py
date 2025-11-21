from django.urls import path
from .views import (
    PlanListCreateView, PlanDetailView,
    CouponListCreateView, CouponDetailView
)

urlpatterns = [
    path("plans/", PlanListCreateView.as_view()),
    path("plans/<int:pk>/", PlanDetailView.as_view()),

    path("coupons/", CouponListCreateView.as_view()),
    path("coupons/<int:pk>/", CouponDetailView.as_view()),
]
