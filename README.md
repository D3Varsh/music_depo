# MusicDepo Scheduling App

This is the **Django-based backend** for the MusicDepo lesson management system. It includes models and logic for scheduling music lessons, assigning instructors and rooms, tracking payments, and managing payroll.

---

## 🧱 Tech Stack

- **Backend**: Django 5.x
- **Database**: PostgreSQL
- **Environment**: Python 3.12+ (recommended with WSL2)
- **ORM**: Django Models
- **Admin Panel**: `/admin` (Django default)

---

## ⚙️ Getting Started (WSL / Ubuntu)

### 1. Clone the Repo

```bash
git clone <repo-url> music_depo
cd music_depo
````

### 2. Create Virtual Environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

> If no `requirements.txt` yet, manually install:

```bash
pip install django psycopg2-binary
```

### 4. Set Up PostgreSQL Database

```bash
sudo -u postgres psql
```

In the prompt:

```sql
CREATE DATABASE musicdepotdb;
CREATE USER musicdepot_user WITH PASSWORD 'password';
ALTER ROLE musicdepot_user SET client_encoding TO 'utf8';
ALTER ROLE musicdepot_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE musicdepotdb TO musicdepot_user;
\q
```

### 5. Configure `settings.py`

Ensure the `DATABASES` section is:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'musicdepotdb',
        'USER': 'musicdepot_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## ▶️ Running the Project

### 6. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run the Dev Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## 💡 Useful Commands

|Command|Purpose|
|---|---|
|`python manage.py shell`|Interact with models in Python shell|
|`python manage.py dbshell`|Open raw SQL shell (psql)|
|`python manage.py runserver`|Launch dev server|
|`python manage.py makemigrations`|Generate DB migrations|
|`python manage.py migrate`|Apply migrations|
|`python manage.py createsuperuser`|Create admin user|

---

## 🧪 Optional: Load Dummy Data

If `core/scripts/populate_dummy_data.py` exists:

```bash
python manage.py shell < core/scripts/populate_dummy_data.py
```

This adds test clients, instructors, rooms, payments, payroll, and schedules.

---

## 🚧 Future Improvements

- Instructor dashboard
    
- Client self-service booking
    
- Email reminders & notifications
    
- REST API integration
    