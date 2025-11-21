import threading
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Subscription
from .serializers import SubscriptionSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    
    # ALL SERVICES ARE ON YOUR LOCALHOST!
    SERVICE_URLS = {
        'doctor': 'http://localhost:8001',      # Doctor service
        'plan': 'http://localhost:8002',        # Plan service
        'plan_features': 'http://localhost:8006', # Plan Features service
        'coupon': 'http://localhost:8003',      # Coupon service
        'agent': 'http://localhost:8005',       # Agent service
        'invoice': 'http://localhost:8004',     # Your Invoice service
    }

    def create(self, request, *args, **kwargs):
        # Create subscription first
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        
        # Trigger async invoice generation
        self.trigger_invoice_generation(subscription)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def trigger_invoice_generation(self, subscription):
        def generate_invoice_async():
            invoice_data = {
                'subscription_id': subscription.subscription_id,
                'doctor_id': subscription.doctor_id,
                'plan_id': subscription.plan_id,
                'amount': subscription.plan_pricee,
                'discount': subscription.discount_amount,
                'final_amount': subscription.plan_pricee - subscription.discount_amount,
                'invoice_number': subscription.invoice
            }
            
            try:
                response = requests.post(
                    f"{self.SERVICE_URLS['invoice']}/api/invoices/generate/",
                    json=invoice_data,
                    timeout=30
                )
                print(f"✅ Invoice created: {response.status_code}")
            except Exception as e:
                print(f"❌ Invoice service error: {str(e)}")
        
        thread = threading.Thread(target=generate_invoice_async)
        thread.daemon = True
        thread.start()