# ElevatePro Internships - Setup Instructions

## 🚀 **Quick Setup Guide**

### 1. **Install Python Dependencies**

First, create a virtual environment and install the required packages:

```bash
# Navigate to project directory
cd c:\xampp\htdocs\olive

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **MySQL Setup with XAMPP**

1. **Start XAMPP**:
   - Open XAMPP Control Panel
   - Start **Apache** and **MySQL** services

2. **Create Database**:
   - Open phpMyAdmin: http://localhost/phpmyadmin
   - Create a new database named `shardel_int`
   - Set charset to `utf8mb4_general_ci`

### 3. **Django Setup**

```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Create and run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

### 4. **Access the Application**

- **Main Site**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

## 🔧 **Troubleshooting**

### MySQL Connection Issues

If you get `MySQLdb module not found` error:

```bash
# Install MySQL client for Python
pip install mysqlclient

# Alternative if above fails:
pip install PyMySQL
```

Then add this to `settings.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Virtual Environment Issues

If virtual environment creation fails:
```bash
# Use alternative method
python -m pip install virtualenv
virtualenv venv
```

### Port Conflicts

If port 8000 is busy:
```bash
python manage.py runserver 8080
```

## 📋 **Initial Data Setup**

1. **Create Admin User**: Use the superuser you created
2. **Create Supervisor Users**: Through admin panel
3. **Create Internships**: Add some sample internship opportunities
4. **Test Application Flow**: Apply as visitor, approve as admin

## 🎯 **Default Credentials**

- **Admin**: Created during setup
- **New Interns**: Password is `intern2024` (configurable in settings)

## 📁 **Project Structure**

```
olive/
├── venv/                     # Virtual environment
├── shaderl_internships/      # Main Django project
├── accounts/                 # User management
├── applications/             # Application system
├── internships/              # Internship management
├── reports/                  # Reports & evaluations
├── dashboard/                # Dashboards
├── templates/                # HTML templates
├── static/                   # CSS, JS, images
└── media/                    # Uploaded files
```
