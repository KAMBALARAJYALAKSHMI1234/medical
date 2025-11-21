Plans Microservice – Django REST Framework

This microservice manages subscription Plans for the Lonbow System.
It provides full CRUD APIs using Django + Django REST Framework + MySQL and includes global exception handling, validation, and Postman-ready JSON examples.

🚀 Features

Create, update, delete plans

List all plans

Retrieve single plan

Boolean field normalization (handles MySQL BIT(1))

Global exception handler with clean error responses

Fully tested Postman API payloads

Proper microservice folder structure

📂 Project Structure
plans_service/
│
├── plans_service/
│   ├── settings.py
│   ├── urls.py
│   ├── exceptions.py      ← Global error formatter
│   └── wsgi.py
│
├── plans/
│   ├── models.py          ← Plan model
│   ├── serializers.py     ← Validation + Bool normalization
│   ├── views.py           ← CRUD Viewsets
│   ├── urls.py            ← /api/plans/ routes
│   └── tests/             ← (Optional)
│
├── .env                   ← DB connection details
├── manage.py
└── README.md

🛢 Database Configuration (.env)
DB_NAME=LBDOC_PYDB
DB_USER=admin
DB_PASSWORD=india123
DB_HOST=localhost
DB_PORT=3306

🧩 Plan Model
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

🌐 API Endpoints
Method	Endpoint	Description
POST	/api/plans/	Create a new plan
GET	/api/plans/	Get all plans
GET	/api/plans/<id>/	Get a specific plan
PATCH	/api/plans/<id>/	Update selected fields
PUT	/api/plans/<id>/	Update entire plan
DELETE	/api/plans/<id>/	Delete a plan
📬 POSTMAN JSON Examples
1️⃣ Create Plan (POST /api/plans/)
{
    "plan_name": "Premium Plan",
    "price": 999,
    "duration": 30,
    "is_active": true
}

2️⃣ Patch Update (PATCH /api/plans/2/)
{
    "price": 1499,
    "is_active": false
}

3️⃣ Full Update (PUT /api/plans/2/)
{
    "plan_name": "Standard Plan Updated",
    "price": 1200,
    "duration": 45,
    "is_active": true
}

⚠️ Global Error Handling

Thanks to custom_exception_handler, all errors return:

Example Validation Error
{
    "errors": {
        "plan_name": ["This field is required."]
    }
}

Example 500 Error
{
    "errors": "Internal server error."
}

🛠 Run the Project
1. Install Dependencies
pip install -r requirements.txt

2. Apply Migrations
python manage.py makemigrations
python manage.py migrate

3. Start Server
python manage.py runserver

🧪 Testing with Postman

Import the API endpoints manually or create a Postman collection.

Recommended test order:

POST → create plan

GET → verify list

PATCH / PUT → update

DELETE → remove

GET → confirm deletion

📌 Notes

MySQL BIT(1) fields return bytes (b'\x00'), this microservice automatically normalizes them.

All boolean fields accept:
"0", "1", "true", "false", 0, 1, true, false.

👨‍💻 Author

Microservice for Lonbow System
Built using Django 5 + DRF + MySQL

If you want, I can also generate:

✅ Dockerfile + docker-compose
✅ OpenAPI (Swagger) documentation
✅ Postman Collection JSON file
✅ README for Doctor Service