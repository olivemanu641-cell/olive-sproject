# ElevatePro Internships - Django Web Application

**ElevatePro Internships** is a modern, comprehensive internship management platform built with Django and MySQL. It streamlines the entire internship lifecycle from application to completion.

## 🌟 **Key Features**

### **New Streamlined Workflow**
1. **Visitors** apply for internships directly (no account creation required)
2. **Admins** review and approve/reject applications
3. **System** automatically creates Intern accounts with standard password upon approval
4. **Interns** login and access their personalized dashboard

### **Role-Based Access Control**
- **Admin**: Full system management, user approval, internship creation
- **Supervisor**: Report review, intern evaluation, performance tracking
- **Intern**: Report submission, progress tracking, profile management

### **Core Functionality**
- 📋 **Application Management**: Streamlined visitor application process
- 🏢 **Internship Opportunities**: Comprehensive internship posting and management
- 📊 **Progress Tracking**: Detailed reporting and evaluation system
- 👥 **User Management**: Role-based access with approval workflows
- 📈 **Analytics Dashboard**: Performance metrics and insights

## 🛠️ **Technology Stack**

- **Backend**: Django 4.2.7 with Python
- **Database**: MySQL (XAMPP compatible)
- **Frontend**: Bootstrap 5 with modern CSS/JavaScript
- **File Handling**: PDF/DOC support for reports and documents
- **Authentication**: Custom user model with role-based permissions

## 📋 **Requirements**

- Python 3.8+
- XAMPP (Apache + MySQL)
- MySQL database named `shardel_int`

## 🚀 **Installation & Setup**

### 1. **Clone and Setup**
```bash
cd c:\xampp\htdocs\olive
pip install -r requirements.txt
```

### 2. **Database Configuration**
- Start XAMPP and ensure MySQL is running
- Create database `shardel_int` in phpMyAdmin
- Update `.env` file if needed (default settings work with XAMPP)

### 3. **Django Setup**
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 4. **Access the Application**
- **Main Site**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

## 📁 **Project Structure**

```
olive/
├── shaderl_internships/          # Main project settings
├── accounts/                     # User management & authentication
├── applications/                 # Visitor application system
├── internships/                  # Internship opportunity management
├── reports/                      # Report submission & evaluation
├── dashboard/                    # Role-based dashboards
├── templates/                    # HTML templates
├── static/                       # CSS, JavaScript, images
├── media/                        # User uploaded files
└── requirements.txt              # Python dependencies
```

## 🎯 **Application Workflow**

### **For Visitors (Applicants)**
1. Browse available internships
2. Submit application with documents (CV, cover letter, etc.)
3. Wait for admin approval
4. Receive login credentials upon approval

### **For Admins**
1. Review incoming applications
2. Approve/reject applications with notes
3. System automatically creates intern accounts
4. Manage internships and supervisors
5. Monitor overall system performance

### **For Supervisors**
1. Review intern reports
2. Provide feedback and ratings
3. Conduct performance evaluations
4. Track intern progress

### **For Interns**
1. Login with provided credentials
2. Submit periodic reports
3. Track progress and feedback
4. Update profile information

## 🔧 **Configuration**

### **Environment Variables (.env)**
```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=shardel_int
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
DEFAULT_INTERN_PASSWORD=intern2024
```

### **Key Settings**
- **Default Intern Password**: `intern2024` (configurable)
- **Currency**: CFA (West African Franc)
- **File Upload Limit**: 10MB
- **Supported File Types**: PDF, DOC, DOCX

## 📊 **Database Models**

### **User Management**
- Custom User model with roles (Admin, Supervisor, Intern)
- Profile model with extended information
- Approval workflow for new users

### **Application System**
- InternshipApplication model for visitor applications
- Automatic account creation upon approval
- Document upload and management

### **Internship Management**
- Internship model with detailed information
- Skill requirements and categorization
- Supervisor assignment

### **Reporting System**
- InternReport model for progress tracking
- Evaluation model for supervisor assessments
- Template system for standardized reports

## 🎨 **Modern UI Features**

- **Responsive Design**: Mobile-first approach
- **Modern Styling**: Clean, professional interface
- **Interactive Elements**: Smooth animations and transitions
- **Role-based Dashboards**: Customized for each user type
- **File Upload Interface**: Drag-and-drop functionality

## 🔐 **Security Features**

- CSRF protection on all forms
- File type validation for uploads
- Role-based access control
- SQL injection protection via Django ORM
- Secure password handling

## 📈 **Future Enhancements**

- Email notifications for application status
- Advanced analytics and reporting
- Chat/messaging system
- Payment integration
- Mobile application
- API endpoints for third-party integration

## 👨‍💻 **Development**

### **Adding New Features**
1. Create models in appropriate app
2. Run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Update admin interface
4. Create views and templates
5. Add URL patterns

### **Customization**
- Modify `settings.py` for configuration changes
- Update templates in `templates/` directory
- Add custom CSS/JS in `static/` directory
- Extend models for additional functionality

## 🆘 **Support**

For issues or questions:
1. Check Django documentation
2. Review error logs in console
3. Ensure XAMPP MySQL is running
4. Verify database connection settings

---

**ElevatePro Internships** - Elevating careers through structured internship management.

*Built with ❤️ using Django and modern web technologies.*
