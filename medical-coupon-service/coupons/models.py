from django.db import models

class Plan(models.Model):
    PLAN_ID = models.AutoField(primary_key=True)
    PLAN_NAME = models.CharField(max_length=64)

    class Meta:
        db_table = "PLANS"

    def __str__(self):
        return self.PLAN_NAME


class Coupon(models.Model):
    COUPON_ID = models.AutoField(primary_key=True)
    PLAN_ID = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        db_column="PLAN_ID"
    )
    COUPON_NAME = models.CharField(max_length=64)
    PERCENTAGE = models.IntegerField()
    ALL_PLANS = models.BooleanField(default=False)
    IS_ACTIVE = models.BooleanField(default=False)
    CREATED_AT = models.DateTimeField(auto_now_add=True)
    UPDATED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "COUPONS"

    def __str__(self):
        return self.COUPON_NAME
