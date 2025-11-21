from django.db import models

class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=64)
    price = models.IntegerField()
    duration = models.IntegerField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "PLANS"

    def __str__(self):
        return self.plan_name
