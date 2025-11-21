from django.db import models

class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    doctor_id = models.PositiveIntegerField()
    plan_id = models.PositiveIntegerField()
    plan_pricee = models.IntegerField()
    discount_amount = models.IntegerField()
    coupon_id = models.PositiveIntegerField(null=True, blank=True)
    plan_start_date = models.DateTimeField()
    plan_end_date = models.DateTimeField()
    invoice = models.CharField(max_length=512)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    agent_id = models.IntegerField()

    class Meta:
        db_table = 'SUBSCRIPTION'  # Maps to existing table
        managed = False  # Don't manage table creation

    def __str__(self):
        return f"Subscription {self.subscription_id}"