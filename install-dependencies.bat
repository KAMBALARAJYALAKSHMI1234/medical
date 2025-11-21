@echo off
echo Installing dependencies for all services...

cd medical-doctor-service
pip install -r requirements.txt
cd ..

cd medical-plan-service
pip install -r requirements.txt
cd ..

cd medical-plan-features-service
pip install -r requirements.txt
cd ..

cd medical-coupon-service
pip install -r requirements.txt
cd ..

cd medical-agent-service
pip install -r requirements.txt
cd ..

cd medical-subscription-service
pip install -r requirements.txt
cd ..

cd medical-invoice-service
pip install -r requirements.txt
cd ..

echo All dependencies installed!
pause