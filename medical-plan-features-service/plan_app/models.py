from django.db import models


class Plan(models.Model):
    PLAN_ID = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'PLANS'
        managed = False  # do NOT let Django create this table


class PlanFeatures(models.Model):
    FEATURE_ID = models.AutoField(primary_key=True)
    PLAN = models.ForeignKey(Plan, on_delete=models.CASCADE, db_column='PLAN_ID')
    FEATURE_NAME = models.CharField(max_length=64)
    FEATURE_COUNT = models.IntegerField()
    IS_ACTIVE = models.BooleanField(default=False)
    CREATED_AT = models.DateTimeField()
    UPDATED_AT = models.DateTimeField()

    class Meta:
        db_table = 'PLAN_FEATURES'
        managed = False  # use your existing SQL table
