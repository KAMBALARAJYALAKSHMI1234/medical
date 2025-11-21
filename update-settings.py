import os

# Service paths and their settings files
services = {
    'subscription': 'medical-subscription-service/subscription_project/settings.py',
    'invoice': 'medical-invoice-service/invoice_project/settings.py',
    'doctor': 'medical-doctor-service/doctor_service/settings.py',
    'plan': 'medical-plan-service/plans_service/settings.py',
    'coupon': 'medical-coupon-service/discount_system/settings.py',
    'agent': 'medical-agent-service/agents_service/settings.py',
    'plan_features': 'medical-plan-features-service/plan_project/settings.py'
}

for service_name, settings_path in services.items():
    if os.path.exists(settings_path):
        print(f"Updating {service_name}...")
        
        with open(settings_path, 'r') as file:
            content = file.read()
        
        # Add CORS to INSTALLED_APPS if not already there
        if "'corsheaders'" not in content:
            content = content.replace("INSTALLED_APPS = [", "INSTALLED_APPS = [\n    'corsheaders',")
        
        # Add CORS middleware if not already there  
        if "'corsheaders.middleware.CorsMiddleware'" not in content:
            content = content.replace("MIDDLEWARE = [", "MIDDLEWARE = [\n    'corsheaders.middleware.CorsMiddleware',")
        
        # Add CORS settings at the end if not already there
        if "CORS_ALLOW_ALL_ORIGINS" not in content:
            content += "\n\n# CORS settings\nCORS_ALLOW_ALL_ORIGINS = True\nCORS_ALLOW_CREDENTIALS = True\n"
        
        with open(settings_path, 'w') as file:
            file.write(content)
        
        print(f"✅ {service_name} updated")
    else:
        print(f"❌ {settings_path} not found")

print("\n🎯 All services updated! Now RESTART all services.")