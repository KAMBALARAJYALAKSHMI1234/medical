import os
import io
import base64
from django.http import HttpResponse
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from .models import Invoice
from .serializers import InvoiceSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def generate_pdf(self, invoice):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Add logo at top
        try:
            logo_path = os.path.join(settings.BASE_DIR, 'WhiteCoats-Logo.png')
            logo = ImageReader(logo_path)
            p.drawImage(logo, 50, height - 150, width=100, height=80, preserveAspectRatio=True)
        except:
            # If logo not found, continue without it
            pass
        
        # Company header with logo
        p.setFillColorRGB(0.2, 0.4, 0.6)  # Blue color
        p.setFont("Helvetica-Bold", 20)
        p.drawString(160, height - 100, "WHITE COATS MEDICAL")
        
        p.setFont("Helvetica", 12)
        p.drawString(160, height - 120, "Professional Healthcare Services")
        p.drawString(160, height - 140, "123 Medical Center, Healthcare City")
        
        # Invoice title
        p.setFillColorRGB(0, 0, 0)  # Black color
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, height - 180, "MEDICAL SUBSCRIPTION INVOICE")
        
        # Separator line
        p.setStrokeColorRGB(0.2, 0.4, 0.6)
        p.setLineWidth(2)
        p.line(50, height - 190, width - 50, height - 190)
        
        # Invoice details
        p.setFont("Helvetica", 12)
        details = [
            (f"Invoice Number: {invoice.invoice_number}", height - 220),
            (f"Subscription ID: {invoice.subscription_id}", height - 240),
            (f"Doctor ID: {invoice.doctor_id}", height - 260),
            (f"Plan ID: {invoice.plan_id}", height - 280),
            ("", height - 300),  # Empty line for spacing
            (f"Plan Amount: ${invoice.amount}", height - 320),
            (f"Discount Applied: ${invoice.discount_amount}", height - 340),
            (f"Final Amount: ${invoice.final_amount}", height - 360),
            ("", height - 380),  # Empty line
            (f"Invoice Date: {invoice.generated_at.strftime('%B %d, %Y')}", height - 400),
            (f"Subscription Period: {invoice.generated_at.strftime('%Y')}", height - 420),
        ]
        
        for text, y_pos in details:
            p.drawString(50, y_pos, text)
        
        # Thank you message
        p.setFont("Helvetica-Oblique", 10)
        p.drawString(50, 100, "Thank you for choosing White Coats Medical Services!")
        p.drawString(50, 80, "Your subscription helps us provide better healthcare solutions.")
        
        # Footer
        p.setFont("Helvetica", 8)
        p.drawString(50, 50, "White Coats Medical • Phone: (555) 123-HEAL • Email: info@whitecoats.com")
        p.drawString(50, 35, "This is a computer-generated invoice. No signature required.")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        file_name = f"{invoice.invoice_number}.pdf"
        
        return buffer, file_name

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """
        Generate and store invoice for a subscription
        """
        data = request.data
        
        # Create invoice record
        invoice_data = {
            'subscription_id': data['subscription_id'],
            'doctor_id': data['doctor_id'],
            'plan_id': data['plan_id'],
            'invoice_number': data['invoice_number'],
            'amount': data['amount'],
            'discount_amount': data['discount'],
            'final_amount': data['final_amount']
        }
        
        serializer = self.get_serializer(data=invoice_data)
        if serializer.is_valid():
            invoice = serializer.save()
            
            # Generate PDF and store in database
            pdf_buffer, file_name = self.generate_pdf(invoice)
            
            # Store PDF in database
            invoice.invoice_file = pdf_buffer.getvalue()
            invoice.invoice_file_name = file_name
            invoice.file_size = len(pdf_buffer.getvalue())
            invoice.is_generated = True
            invoice.save()
            
            return Response({
                'invoice_id': invoice.invoice_id,
                'invoice_number': invoice.invoice_number,
                'message': 'Invoice generated with White Coats logo',
                'download_url': f'/api/invoices/{invoice.invoice_id}/download/',
                'file_size': invoice.file_size
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download invoice PDF with logo
        """
        invoice = self.get_object()
        
        if not invoice.is_generated or not invoice.invoice_file:
            return Response({'error': 'Invoice not generated yet'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create response with PDF file
        response = HttpResponse(
            invoice.invoice_file, 
            content_type='application/pdf'
        )
        
        response['Content-Disposition'] = f'attachment; filename="{invoice.invoice_file_name}"'
        response['Content-Length'] = invoice.file_size
        
        return response