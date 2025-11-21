from rest_framework import routers
from .views import AgentViewSet

router = routers.DefaultRouter()
router.register(r'agents', AgentViewSet, basename='agent')

urlpatterns = router.urls
