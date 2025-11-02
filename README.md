
# Real Estate Management System

A Django-based real estate management system with property listings, user authentication, and inquiry functionality. See `requirements.txt` for dependencies and `realestate_project/settings.py` for configuration.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Frontend](#frontend-templates--static)
- [Authentication](#authentication)
- [Inquiry System](#inquiry-system)
- [Testing](#testing)
- [Sample Data](#sample-data)
- [Contributing](#contributing)

## Features

✅ **Property Management**
- Full CRUD operations for property listings
- Multiple property types (House, Apartment, Condo, etc.)
- Property status tracking (Available, Sold, Pending, Rented)
- Image upload support (featured image + gallery)
- Detailed property specifications

✅ **User Authentication & Authorization**
- User registration and login system
- Role-based access (Agent vs Buyer)
- User profiles with contact information
- Protected routes and ownership validation

✅ **Advanced Search & Filtering**
- Location-based search
- Filter by property type, price range, bedrooms
- Multiple sorting options
- Pagination with filter preservation

✅ **Inquiry System**
- Property inquiries with notifications
- Inquiry management dashboard
- Read/unread status tracking
- Separate views for received/sent inquiries

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd realestatemanagement
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Load sample data (optional):
   ```bash
   python manage.py loaddata fixtures/users.json fixtures/profiles.json fixtures/properties.json fixtures/inquiries.json
   ```

6. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application:
   - Homepage: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Frontend (templates & static)

This project uses Bootstrap 5 for the frontend templates and includes a small set of templates and static files for property management.

Templates:
- `templates/base.html` — base template with navbar, messages and footer
- `templates/properties/property_list.html` — property listing (cards + pagination)
- `templates/properties/property_detail.html` — detailed view with gallery and sidebar
- `templates/properties/property_form.html` — create/edit form
- `templates/properties/property_confirm_delete.html` — delete confirmation

Static files:
- `static/css/style.css` — custom styles and responsive tweaks
- `static/js/main.js` — client-side interactions (image preview, alerts auto-dismiss, simple lightbox)
- `static/images/` — place logos or placeholder images here (placeholder image should be added separately)

Notes:
- Templates reference a placeholder image at `static/images/placeholder-property.jpg`. Add a suitable placeholder image under that path or update the templates to point to a different image.
- For development, Django serves static files automatically. In production, run `python manage.py collectstatic` and configure your web server.

## Authentication

This project includes a simple authentication system with user profiles.

- Custom `UserProfile` model is available in `apps.accounts.models` and is auto-created on user registration.
- User roles: Agent (can list properties) and Buyer (can browse properties).
- Authentication URLs:
	- Login: `/accounts/login/`
	- Register: `/accounts/register/`
	- Profile: `/accounts/profile/`
	- Logout: `/accounts/logout/`

Notes:
- `LOGIN_URL` is configured as `accounts:login` in `realestate_project/settings.py`.
- After registering, users are automatically logged in and redirected to the property list.
- Property create/update/delete views require authentication; use the navigation links to register/login.

## Inquiry System

A property inquiry and contact management system allowing authenticated users to send inquiries about properties.

Features:
- Authenticated users can send inquiries about properties
- Property owners receive email notifications for new inquiries (console backend for MVP)
- Inquiry form on property detail page with pre-filled user information
- Separate views for received inquiries (property owners) and sent inquiries (buyers)
- Mark inquiries as read/unread
- Inquiry detail view with full message and contact information
- Dashboard integration showing recent inquiries
- Admin panel for inquiry management

Inquiry Workflow:
1. **Sending an Inquiry:**
   - Browse properties and open a property detail page
   - If not logged in, click "Login to Inquire" button
   - If logged in and not the property owner, fill out the inquiry form in the sidebar
   - Form is pre-filled with your name, email, and phone (if available)
   - Write your message and click "Send Inquiry"
   - Property owner receives email notification (printed to console in development)
   - Confirmation message appears on success

2. **Managing Inquiries (Property Owners/Agents):**
   - View inquiry count badge on property detail page
   - Access "View Inquiries" from property detail or profile page
   - See all received inquiries with filter tabs
   - Click on inquiry to view full details
   - Reply via email directly from inquiry detail page
   - Inquiries are automatically marked as read when viewed

3. **Tracking Sent Inquiries (Buyers):**
   - View your sent inquiries from profile page
   - See inquiry status (read/unread)
   - Access inquiry details to review your message
   - Contact property owner directly from inquiry detail

Inquiry URLs:
- Send inquiry: `/property/<id>/inquiry/` (POST)
- View inquiries: `/inquiries/?filter=received` or `/inquiries/?filter=sent`
- Inquiry detail: `/inquiry/<id>/`

Email Notifications:
- Development: Emails are printed to console (EMAIL_BACKEND = console)
- Production: Configure SMTP settings in settings.py
- Notification includes: inquirer name, contact info, message, and property link

Admin Features:
- View all inquiries in admin panel
- Filter by read status, date, property type
- Search by property, user, or message content
- Bulk mark as read/unread
- Quick edit read status from list view

Technical Implementation:
- Inquiry model with ForeignKeys to Property and User
- InquiryForm with Bootstrap styling and auto-fill
- Email notifications using Django's send_mail
- Permission checks (only authenticated users can inquire, only involved parties can view)
- Optimized queries with select_related for performance
- Responsive design for mobile inquiry submission

## Testing

### Running Tests

**Run all tests:**
```bash
python manage.py test
```

**Run tests for specific app:**
```bash
python manage.py test apps.properties
python manage.py test apps.accounts
```

**Run specific test class:**
```bash
python manage.py test apps.properties.tests.PropertyModelTest
```

**Run with verbose output:**
```bash
python manage.py test --verbosity=2
```

**Run with coverage:**
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Test Coverage

The test suite includes:

**Model Tests:**
- Property, PropertyImage, Inquiry model creation and validation
- UserProfile model and signal-based creation
- Model relationships and constraints
- Field validations and default values
- Custom model methods and properties

**View Tests:**
- Property CRUD operations
- Authentication and authorization checks
- Search and filter functionality
- Inquiry submission and management
- User registration and login flows

**Form Tests:**
- Property creation/edit form validation
- Inquiry form submission and validation
- User registration form
- Profile update form
- Search and filter form

**Integration Tests:**
- Complete user workflows
- Multi-step processes (register → create property → receive inquiry)
- Permission and ownership validation
- Email notification system
- File upload handling

For detailed testing procedures and manual testing checklists, see `TESTING.md`.

## Sample Data

The project includes sample data fixtures for demo and testing purposes.

### Loading Fixtures

```bash
python manage.py loaddata users profiles properties inquiries
```

### Sample Accounts

| Username | Password | Role | Properties |
|----------|----------|------|------------|
| admin | admin123 | Superuser | 0 |
| john_agent | agent123 | Agent | 5 |
| sarah_agent | agent123 | Agent | 5 |
| mike_buyer | buyer123 | Buyer | 0 |
| emma_buyer | buyer123 | Buyer | 0 |

### Sample Data Details

Fixtures include:
- 15 diverse property listings
- 10 sample inquiries
- 5 users with profiles
- Various property types and locations
- Price range: $200K - $1.25M
- Locations across major US cities

See `fixtures/README.md` for complete fixture documentation.

## Contributing

### Areas for Enhancement
- Advanced image gallery with multiple upload
- Property comparison feature
- Saved searches and favorites
- Real-time chat between buyers and agents
- Property analytics and reporting
- Map integration
- Email templates for notifications
- Mobile app development

### Development Guidelines
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

See `CONTRIBUTING.md` for detailed contribution guidelines.
