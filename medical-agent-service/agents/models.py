from django.db import models

class Agent(models.Model):
    agent_id = models.AutoField(db_column='AGENT_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=64)
    designation = models.CharField(db_column='DESIGNATION', max_length=64)
    mobileno = models.CharField(db_column='MOBILENO', max_length=16)
    email = models.CharField(db_column='EMAIL', max_length=64)
    password = models.CharField(db_column='PASSWORD', max_length=255)
    remarks = models.CharField(db_column='REMARKS', max_length=512)
    is_active = models.BooleanField(db_column='IS_ACTIVE')
    created_at = models.DateTimeField(db_column='CREATED_AT')
    updated_at = models.DateTimeField(db_column='UPDATED_AT')
    is_admin = models.BooleanField(db_column='IS_ADMIN')

    class Meta:
        db_table = 'AGENTS'
        managed = False
