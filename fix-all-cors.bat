@echo off
echo Installing CORS for all services...

cd medical-subscription-service
pip install django-cors-headers
echo ✅ Subscription - CORS installed
cd ..

cd medical-invoice-service
pip install django-cors-headers
echo ✅ Invoice - CORS installed
cd ..

cd medical-doctor-service
pip install django-cors-headers
echo ✅ Doctor - CORS installed
cd ..

cd medical-plan-service
pip install django-cors-headers
echo ✅ Plan - CORS installed
cd ..

cd medical-coupon-service
pip install django-cors-headers
echo ✅ Coupon - CORS installed
cd ..

cd medical-agent-service
pip install django-cors-headers
echo ✅ Agent - CORS installed
cd ..

cd medical-plan-features-service
pip install django-cors-headers
echo ✅ Plan Features - CORS installed
cd ..

echo.
echo 🎯 NOW update each service's settings.py file with CORS configuration!
echo.
pause