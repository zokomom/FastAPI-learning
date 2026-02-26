# 🚀 InteractHub – RESTful Social Media Backend API

🔗 **Live API:** https://interacthub-wfkm.onrender.com/  
> 🚀 Cold start Alert !! : First request may take ~15–20 seconds. The server boots, stretches, and then gets to work.

📄 **Swagger Docs:** https://interacthub-wfkm.onrender.com/docs  

📘 **ReDoc:** https://interacthub-wfkm.onrender.com/redoc  

>### InteractHub is a modular RESTful backend application built using FastAPI and PostgreSQL. It provides core social media features including user authentication, post creation, retrieval, and like functionality.
---

## 🧠 Features

- User Registration & Login (JWT Authentication)
- Secure Password Hashing
- Create, Read, Update, Delete Posts
- Like / Unlike Posts
- Pagination & Search using Query Parameters
- Relational Database Modeling (Users ↔ Posts ↔ Likes)
- Alembic Migrations
- Input Validation using Pydantic
- Fully Tested APIs using Postman

---

## 🛠️ Tech Stack

**Backend Framework**
- FastAPI

**Database**
- PostgreSQL
- SQLAlchemy (ORM)
- Alembic (Migrations)

**Authentication**
- OAuth2 with JWT Tokens
- Passlib (Password Hashing)

**Testing**
- Postman

**Deployment**
- Render / Railway (Cloud Deployment)

---
```
## 📂 Project Structure
    app/
    │
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── oauth2.py
    ├── routers/
    │ ├── users.py
    │ ├── posts.py
    │ └── auth.py
    │
    alembic/
    requirements.txt
```
---

## 🔐 Authentication Flow

- User registers with email & password
- Password is hashed before storing in DB
- On login, JWT access token is generated
- Protected routes require Bearer Token
- Token is verified before allowing access

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/interacthub.git
cd interacthub
```
### 2️⃣ Create Virtual Environment & Install Dependencies

```bash 
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
``` 
### 4️⃣ Setup Environment Variables
Create a `.env` file in the root directory with the following content:

```env  
DATABASE_URL=postgresql://username:password@localhost:5432/interacthub
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
### 5️⃣ Run Database Migrations

```bash
alembic upgrade head
``` 
### 6️⃣ Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```
### 7️⃣ Access API Documentation
Open your browser and navigate to `http://localhost:8000/docs` to explore the interactive API documentation provided by FastAPI.
### 🧪 Testing the API
Use Postman or any API testing tool to interact with the endpoints.

## 🧱 Database Design

### Users Table
- **id** (Primary Key)
- **email** (Unique)
- **password** (Hashed)
- **created_at**

### Posts Table
- **id** (Primary Key)
- **title**
- **content**
- **published**
- **owner_id** (Foreign Key → Users)

### Likes Table
- **user_id** (Foreign Key)
- **post_id** (Foreign Key)
- **Composite Primary Key** (user_id, post_id)

## 📌 Key Backend Concepts Demonstrated

- **RESTful API Design**
- **Dependency Injection**
- **Database Relationships** (One-to-Many, Many-to-Many)
- **Token-Based Authentication**
- **Environment Variable Management**
- **Production-Ready Project Structure**
- **Migration-Based Schema Management**

## 📈 Future Improvements

- Dockerize the application
- Add Unit & Integration Tests (pytest)
- Implement Role-Based Authorization
- Add Rate Limiting
- CI/CD Integration
- Caching (Redis)

## 👨‍💻 Author

**Atharv Kumar**  
BCA Final Year Student  
Aspiring Backend Developer

## 📜 License

This project is built for learning and portfolio purposes.
