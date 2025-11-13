# CENTRALIZED ADMIN MANAGEMENT WITH ROLE BASED ACCESS CONTROL

**Academic Project for Bachelor of Technology in Computer Science and Technology**

## Project Overview

This project implements a centralized admin management system with role-based access control for e-commerce platforms. The system enables secure management of users, products, orders, and deliveries through a web-based interface with different access levels based on user roles.

## Team Members



- - **D.V. SAI GANESH** (213C1A0509)
- - **M. RADHA KRISHNA** (213C1A0521)
- - **K. JEEVANA REKHA** (213C1A0519)

**Institution:** D.M.S.S.V.H College of Engineering, Machilipatnam  
**Guide:** Smt. N. Sushma, M.Tech (Associate Professor, Department of CSE)  
**Academic Year:** 2024-2025

## Key Features

### Core Functionalities
- **Secure Authentication System** - Login/logout with session management
- **Role-Based Access Control** - Different permissions for Admin, Seller, Customer, and Logistics roles
- **Product Management** - Add, edit, delete, and view products with category support
- **Order Management** - Track order status (Pending, Shipped, Delivered, Cancelled)
- **User Management** - Assign and modify user roles and permissions
- **Seller Approval System** - Automated approval workflow for new sellers
- **Logistics Partner Management** - Manage delivery partner approvals
- **Real-time Dashboard** - Comprehensive admin dashboard with analytics

### Security Features
- Protection against XSS, CSRF, and SQL injection attacks
- Secure password handling and session management
- Role-based permission enforcement
- Data integrity validation

## Technology Stack

### Backend
- **Framework:** Django (Python)
- **Database:** SQLite (Development) / MySQL (Production)
- **Authentication:** Django's built-in authentication system
- **Architecture:** Model-View-Template (MVT) pattern

### Frontend
- **Languages:** HTML5, CSS3, JavaScript
- **Styling:** Custom CSS with responsive design
- **UI Components:** Bootstrap integration
- **Template Engine:** Django Templates

### Development Tools
- **IDE:** Visual Studio Code
- **Version Control:** Git & GitHub
- **Testing:** Django Testing Framework
- **Browser Support:** Chrome, Firefox, Safari

## System Requirements

### Hardware Requirements
- **Processor:** Intel Core i3 or higher
- **RAM:** Minimum 8 GB
- **Storage:** Minimum 320 GB

### Software Requirements
- **Python:** 3.8 or higher
- **Django:** Latest stable version
- **Database:** SQLite/MySQL/PostgreSQL
- **OS:** Windows 10+, macOS, or Linux
- **Browser:** Modern web browser

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/saiganeshdenaboina/Academic_Project
cd acedamic_project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install django
pip install pillow  # for image handling
pip install django-widget-tweaks
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the Application
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## Project Structure

```
acedamic_project/
├── accounts/          # User authentication and role management
├── products/          # Product management system
├── orders/           # Order processing and tracking
├── vendors/          # Seller management
├── logistics/        # Delivery partner management
├── cart/             # Shopping cart functionality
├── adminpanel/       # Central admin dashboard
├── templates/        # HTML templates
├── static/           # CSS, JS, images
├── media/            # Uploaded files
├── db.sqlite3        # Database file
└── manage.py         # Django management script
```

## User Roles & Permissions

### Super Admin
- Full system access
- User role management
- System configuration
- Complete CRUD operations

### Admin
- Product management
- Order processing
- User monitoring
- Report generation

### Seller/Vendor
- Product listing (subject to approval)
- Order fulfillment
- Inventory management
- Sales analytics

### Customer
- Product browsing
- Order placement
- Order tracking
- Profile management

### Logistics
- Delivery assignment
- Status updates
- Route management
- Performance tracking

## Testing

The project includes comprehensive testing:

- **Unit Testing** - Individual component testing
- **Integration Testing** - Module interaction testing
- **System Testing** - End-to-end functionality testing
- **User Acceptance Testing** - Real-world usage validation

### Run Tests
```bash
python manage.py test
```

## API Documentation

The system provides RESTful endpoints for:
- User authentication
- Product operations
- Order management
- Role assignments

## Security Measures

- Django's built-in security features
- Input validation and sanitization
- Role-based access control
- Secure session management
- Protection against common web vulnerabilities

## Future Enhancements

- **Analytics Dashboard** - Advanced reporting with charts and graphs
- **Mobile App Integration** - RESTful API development
- **Email Notifications** - Automated email system for order updates
- **AI Recommendations** - Machine learning-based product suggestions
- **Performance Optimization** - Caching and database indexing
- **Multi-language Support** - Internationalization features

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is developed for academic purposes as part of the Bachelor of Technology program at D.M.S.S.V.H College of Engineering.

## Acknowledgments

- **Prof. Dr. T. Ravi Kumar** - Principal, DMSSVH College of Engineering
- **Smt. N. Sushma** - Project Guide and Associate Professor
- **Sri. D. Chinna Venkataswamy** - Internship Trainer, App Genesis Soft Solutions
- **AICTE & APSCHE** - For internship recognition and support

## Contact Information

For queries and support, please contact the development team through the college department.



**Note:** This project is part of academic coursework and demonstrates the practical implementation of web development concepts using Django framework with emphasis on security and role-based access control.
