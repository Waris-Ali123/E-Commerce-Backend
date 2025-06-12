# E-commerce Backend System Using FastAPI

## 📘 Project Overview

This project is a RESTful backend API for an e-commerce platform built with FastAPI. It supports:

* Admin product management
* User authentication
* Product browsing
* Cart management
* Order processing

The API is designed to be secure, maintainable, and scalable, following best practices for FastAPI development.

---

## ✨ Purpose

To provide a robust backend system for an e-commerce application, enabling:

* ✅ Admin CRUD operations for product management
* ✅ User authentication (signup, signin, forgot password, reset password)
* ✅ Public product browsing with filters and search
* ✅ Shopping cart functionality and dummy checkout
* ✅ Order history and details

---

## 🧾 Prerequisites

* Python 3.9+
* Postman (for API testing)
* Knowledge of RESTful APIs
* SQLite (used as the database)

---

## 🛠️ Technology Stack

| Component      | Tool                  |
| -------------- | --------------------- |
| Framework      | FastAPI               |
| Database       | SQLite + SQLAlchemy   |
| Authentication | JWT (PyJWT)           |
| Validation     | Pydantic              |
| Migrations     | Alembic               |
| Password Hash  | bcrypt                |
| Logging        | Python logging module |
| Server         | Uvicorn               |

---

## 🗂 Project Structure

```
python_project/
├── alembic/
│   ├── versions/
│   ├── env.py
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   ├── auth/
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   ├── utils.py
│   ├── products/
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   ├── cart/
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   ├── orders/
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   ├── checkout/
│   │   ├── crud.py
│   │   ├── routes.py
│   ├── exceptions/
│   │   ├── handlers.py
│   ├── utils/
│   │   └── email_sender.py
├── .gitignore
├── alembic.ini
├── requirements.txt
└── .env
```

---

## 🥺 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository_url>
cd python_project
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root:

```env
DATABASE_URL=sqlite:///./ecommerce.db
JWT_SECRET_KEY=<your-secret-key>
JWT_ALGORITHM=HS256
EMAIL_SENDER=<your-email-service-sender>
EMAIL_API_KEY=<your-email-service-api-key>
```

### 5. Run Database Migrations

```bash
alembic upgrade head
```

### 6. Seed Initial Data

```bash
python seed_data.py
```

### 7. Start the Server

```bash
uvicorn app.main:app --reload
```

Visit: [http://localhost:8000](http://localhost:8000)
Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔍 API Testing

Import `postman_collection.json` into Postman.

### Key Endpoints

* **Auth**: `/auth/signup`, `/auth/signin`, `/auth/forgot-password`, `/auth/reset-password`
* **Admin Products**: `/admin/products` (CRUD operations)
* **Public Products**: `/products`, `/products/search`, `/products/{id}`
* **Cart**: `/cart` (add, view, update, delete)
* **Checkout**: `/checkout`
* **Orders**: `/orders`, `/orders/{order_id}`

---

## 🔐 Security Features

* Passwords hashed using **bcrypt**
* JWT authentication with **RBAC (Role-Based Access Control)**
* Secure password reset tokens with expiration
* Input validation with **Pydantic**
* API logging with **Python logging module**

---

## 🧬 Database Schema

| Table                   | Description                                               |
| ----------------------- | --------------------------------------------------------- |
| **Users**               | id, name, email, hashed\_password, role                   |
| **Products**            | id, name, description, price, stock, category, image\_url |
| **Cart**                | id, user\_id, product\_id, quantity                       |
| **PasswordResetTokens** | id, user\_id, token, expiration\_time, used               |
| **Orders**              | id, user\_id, total\_amount, status, created\_at          |
| **OrderItems**          | id, order\_id, product\_id, quantity, price\_at\_purchase |

---

## 🚒 Error Handling Format

All errors follow a consistent JSON format:

```json
{
  "error": true,
  "message": "<Error description>",
  "code": <status_code>
}
```

---

## 🚀 Deployment Notes

* Use **Uvicorn** in production
* Store secrets in **.env** (not hardcoded)
* Always back up the database before migrations

---

## ✅ Testing

* Manual testing of authentication, product CRUD, cart, checkout, and orders

---

## 🚧 Future Improvements

* Add unit tests with **pytest**
* Implement **rate limiting**
* Integrate with **multiple payment gateways**
