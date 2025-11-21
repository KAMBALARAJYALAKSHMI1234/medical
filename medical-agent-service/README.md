
# Agents Microservice 


A simple Django REST microservice for managing agents using full CRUD operations.  
Authentication and role-based access are disabled to make testing easy in Postman.
---

## 📌 Features
- Create a new agent  
- List all agents  
- Retrieve a single agent  
- Update an agent  
- Delete an agent  

---

## 📁 Project Structure


agents_microservice/
│── agents_service/
│── agents/
│── manage.py
│── requirements.txt
│── README.md


---

## 🛠 Setup Instructions

### 1. Create virtual environment


python -m venv venv


### 2. Activate virtual environment
**Windows**


venv\Scripts\activate


**Mac/Linux**


source venv/bin/activate


### 3. Install dependencies


pip install -r requirements.txt


### 4. Run migrations


python manage.py makemigrations
python manage.py migrate


### 5. Start server (Port 8005)


python manage.py runserver 8005


Server URL:  
http://127.0.0.1:8005/

---

## 📡 API Endpoints (Use in Postman)

### ➤ Create Agent (POST)


POST http://127.0.0.1:8005/api/v1/agents/

Body:
```json
{
  "name": "John Doe",
  "designation": "Sales Manager",
  "mobileno": "9876543210",
  "email": "john@example.com",
  "remarks": "New agent added"
}

➤ List All Agents (GET)
GET http://127.0.0.1:8005/api/v1/agents/

➤ Retrieve Single Agent (GET)
GET http://127.0.0.1:8005/api/v1/agents/<id>/


Example:

GET http://127.0.0.1:8005/api/v1/agents/1/

➤ Update Agent (PUT)
PUT http://127.0.0.1:8005/api/v1/agents/1/


Body:

{
  "name": "John Updated",
  "designation": "Senior Manager",
  "mobileno": "9999999999",
  "email": "john_updated@example.com",
  "remarks": "Updated info"
}

➤ Delete Agent (DELETE)
DELETE http://127.0.0.1:8005/api/v1/agents/1/

✔ Database

Uses default SQLite unless you configure MySQL manually.