from django.contrib import admin
from .models import Agent

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('agent_id','name','email','mobileno','designation','is_active','is_admin','created_at')
    readonly_fields = ('agent_id','created_at','updated_at')
