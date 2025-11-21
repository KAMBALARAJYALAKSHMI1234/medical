from django.db import models

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    subscription_id = models.PositiveIntegerField()
    doctor_id = models.PositiveIntegerField()
    plan_id = models.PositiveIntegerField()
    invoice_number = models.CharField(max_length=512)
    amount = models.IntegerField()
    discount_amount = models.IntegerField()
    final_amount = models.IntegerField()
    invoice_file = models.BinaryField(null=True, blank=True)  # Store PDF in database
    invoice_file_name = models.CharField(max_length=255, null=True, blank=True)
    file_size = models.IntegerField(default=0)
    generated_at = models.DateTimeField(auto_now_add=True)
    is_generated = models.BooleanField(default=False)

    class Meta:
        db_table = 'INVOICES'
        managed = False

    def __str__(self):
        return f"Invoice {self.invoice_number}"