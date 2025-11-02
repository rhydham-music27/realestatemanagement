# Testing Guide

This document provides detailed manual testing procedures for the Real Estate Management System.

## Table of Contents
- [Automated Tests](#automated-tests)
- [Manual Testing Procedures](#manual-testing-procedures)
- [Test Scenarios](#test-scenarios)
- [Browser Compatibility](#browser-compatibility)
- [Performance Testing](#performance-testing)

## Automated Tests

### Running the Test Suite

```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific app tests
python manage.py test apps.properties
python manage.py test apps.accounts

# Run specific test class
python manage.py test apps.properties.tests.PropertyModelTest

# Run specific test method
python manage.py test apps.properties.tests.PropertyModelTest.test_property_creation
```

### Test Coverage

Install coverage tool:
```bash
pip install coverage
```

Run tests with coverage:
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates htmlcov/index.html
```

Open `htmlcov/index.html` in browser to view detailed coverage report.

### Expected Test Results

- **Total Tests:** 50+ tests across both apps
- **Expected Pass Rate:** 100%
- **Coverage Target:** 80%+ for models and views

## Manual Testing Procedures

### 1. User Registration and Authentication

#### Test Case 1.1: User Registration (Agent)
**Steps:**
1. Navigate to http://127.0.0.1:8000/accounts/register/
2. Fill in registration form:
   - Username: test_agent
   - First Name: Test
   - Last Name: Agent
   - Email: test@agent.com
   - Password: TestPass123!
   - Confirm Password: TestPass123!
   - Role: Agent
3. Click "Register"

**Expected Results:**
- User is created successfully
- User is automatically logged in
- Redirected to property list page
- Success message displayed: "Registration successful!"
- Profile is auto-created with Agent role
- Navigation shows "Add Property" link

#### Test Case 1.2: User Registration (Buyer)
**Steps:**
1. Logout if logged in
2. Navigate to registration page
3. Register as Buyer with different credentials

**Expected Results:**
- User created with Buyer role
- No "Add Property" link in navigation
- Can browse properties but cannot create

#### Test Case 1.3: User Login
**Steps:**
1. Logout
2. Navigate to http://127.0.0.1:8000/accounts/login/
3. Enter valid credentials
4. Click "Login"

**Expected Results:**
- Successful login
- Welcome message displayed
- Redirected to property list
- User menu shows username and profile link

#### Test Case 1.4: Invalid Login
**Steps:**
1. Try logging in with incorrect password

**Expected Results:**
- Login fails
- Error message displayed
- User remains on login page

#### Test Case 1.5: Logout
**Steps:**
1. Click logout in user menu

**Expected Results:**
- User logged out
- Logout message displayed
- Redirected to property list
- Navigation shows Login/Register links

### 2. Property CRUD Operations

#### Test Case 2.1: Create Property (Agent)
**Steps:**
1. Login as agent
2. Click "Add Property" in navigation
3. Fill out property form:
   - Title: Test Property
   - Description: Beautiful test property
   - Price: 500000
   - Address: 123 Test St
   - City: Test City
   - State: Test State
   - Zipcode: 12345
   - Bedrooms: 3
   - Bathrooms: 2.5
   - Area: 2000
   - Property Type: House
   - Status: Available
   - Upload featured image (optional)
4. Click "Add Property"

**Expected Results:**
- Property created successfully
- Success message displayed
- Redirected to property list
- New property appears in list
- Owner is set to current user

#### Test Case 2.2: Create Property (Buyer - Should Fail)
**Steps:**
1. Login as buyer
2. Try to access /property/new/ directly

**Expected Results:**
- Access denied or no "Add Property" button visible
- If accessed directly, should redirect or show error

#### Test Case 2.3: View Property Detail
**Steps:**
1. Click on any property card

**Expected Results:**
- Property detail page loads
- All property information displayed
- Featured image shown (or placeholder)
- Specifications visible (beds, baths, area)
- Location information displayed
- If owner: Edit/Delete buttons visible
- If not owner: Inquiry form visible

#### Test Case 2.4: Edit Property (Owner)
**Steps:**
1. Login as property owner
2. Navigate to property detail
3. Click "Edit" button
4. Modify property details
5. Click "Update Property"

**Expected Results:**
- Edit form pre-filled with current data
- Changes saved successfully
- Success message displayed
- Redirected to property list
- Updated data visible

#### Test Case 2.5: Edit Property (Non-Owner - Should Fail)
**Steps:**
1. Login as different user
2. Try to access /property/<id>/edit/ for property owned by another user

**Expected Results:**
- Access denied (404 or permission error)
- Cannot edit other users' properties

#### Test Case 2.6: Delete Property (Owner)
**Steps:**
1. Login as property owner
2. Navigate to property detail
3. Click "Delete" button
4. Confirm deletion

**Expected Results:**
- Confirmation page displayed
- Property details shown for verification
- After confirmation, property deleted
- Success message displayed
- Property no longer appears in list
- Related images also deleted

#### Test Case 2.7: Delete Property (Non-Owner - Should Fail)
**Steps:**
1. Try to delete property owned by another user

**Expected Results:**
- Access denied
- Property not deleted

### 3. Search and Filter Functionality

#### Test Case 3.1: Location Search
**Steps:**
1. Navigate to property list
2. Expand filter panel
3. Enter city name in search field
4. Click "Apply Filters"

**Expected Results:**
- Only properties in that city displayed
- Filter badge shows active filter
- URL contains search parameter
- Results count updated

#### Test Case 3.2: Property Type Filter
**Steps:**
1. Select "House" from property type dropdown
2. Apply filters

**Expected Results:**
- Only houses displayed
- Other property types hidden
- Filter preserved in URL

#### Test Case 3.3: Price Range Filter
**Steps:**
1. Set min price: 300000
2. Set max price: 600000
3. Apply filters

**Expected Results:**
- Only properties in price range shown
- Properties outside range hidden
- Both filters shown in active filters

#### Test Case 3.4: Bedrooms/Bathrooms Filter
**Steps:**
1. Set minimum bedrooms: 3
2. Set minimum bathrooms: 2
3. Apply filters

**Expected Results:**
- Only properties with 3+ bedrooms and 2+ bathrooms shown
- Filters work as minimum values (inclusive)

#### Test Case 3.5: Combined Filters
**Steps:**
1. Apply multiple filters:
   - Location: New York
   - Property Type: Apartment
   - Min Price: 400000
   - Bedrooms: 2
2. Apply filters

**Expected Results:**
- All filters applied simultaneously
- Only properties matching ALL criteria shown
- All active filters displayed as badges
- URL contains all parameters

#### Test Case 3.6: Sorting
**Steps:**
1. Select "Price: Low to High" from sort dropdown

**Expected Results:**
- Properties automatically re-sorted
- Cheapest properties appear first
- Sort persists across pagination

#### Test Case 3.7: Clear Filters
**Steps:**
1. Apply several filters
2. Click "Clear Filters" button

**Expected Results:**
- All filters removed
- All available properties shown
- Filter badges disappear
- URL reset to default
- Filter panel collapses

#### Test Case 3.8: Filter Persistence with Pagination
**Steps:**
1. Apply filters
2. Navigate to page 2
3. Check if filters still active

**Expected Results:**
- Filters maintained on page 2
- Same filtered results, different page
- URL contains both filter and page parameters

### 4. Inquiry System

#### Test Case 4.1: Send Inquiry (Authenticated Buyer)
**Steps:**
1. Login as buyer
2. Navigate to property detail (not owned by buyer)
3. Fill out inquiry form:
   - Name: (pre-filled)
   - Email: (pre-filled)
   - Phone: (optional)
   - Message: "I'm interested in this property..."
4. Click "Send Inquiry"

**Expected Results:**
- Inquiry submitted successfully
- Success message displayed
- Email notification sent to property owner (check console)
- Inquiry saved in database
- Buyer can see inquiry in "My Inquiries"

#### Test Case 4.2: Send Inquiry (Unauthenticated - Should Fail)
**Steps:**
1. Logout
2. Navigate to property detail
3. Try to submit inquiry

**Expected Results:**
- Inquiry form not visible
- "Login to Inquire" button shown
- Clicking button redirects to login with ?next parameter
- After login, returns to property page

#### Test Case 4.3: Owner Cannot Inquire About Own Property
**Steps:**
1. Login as property owner
2. Navigate to own property detail

**Expected Results:**
- No inquiry form visible
- "View Inquiries" button shown instead
- Shows inquiry count

#### Test Case 4.4: View Received Inquiries (Property Owner)
**Steps:**
1. Login as agent with properties
2. Navigate to /inquiries/?filter=received

**Expected Results:**
- List of inquiries for owner's properties
- Shows inquirer name, property, message preview
- Unread inquiries marked with badge
- Can click to view full details

#### Test Case 4.5: View Sent Inquiries (Buyer)
**Steps:**
1. Login as buyer who sent inquiries
2. Navigate to /inquiries/?filter=sent

**Expected Results:**
- List of inquiries sent by buyer
- Shows property, owner, status (read/unread)
- Can click to view full details

#### Test Case 4.6: View Inquiry Detail
**Steps:**
1. Click on an inquiry from list

**Expected Results:**
- Full inquiry details displayed
- Property information shown
- Contact information visible
- Full message displayed
- If owner: "Reply via Email" button
- If inquirer: property and owner info
- Inquiry marked as read (if owner viewing)

#### Test Case 4.7: Email Notification
**Steps:**
1. Submit an inquiry
2. Check terminal/console output

**Expected Results:**
- Email printed to console (console backend)
- Contains: subject, recipient, message body
- Includes inquirer contact info
- Includes property link

#### Test Case 4.8: Inquiry Dashboard Integration
**Steps:**
1. Login as agent
2. Navigate to profile page

**Expected Results:**
- Recent inquiries section visible
- Shows unread inquiry count
- Displays last 5 inquiries
- Link to view all inquiries

### 5. User Profile Management

#### Test Case 5.1: View Profile
**Steps:**
1. Login
2. Click profile link in user menu

**Expected Results:**
- Profile page loads
- User information displayed
- Role badge shown
- User's properties listed (if agent)
- Recent inquiries shown
- Edit forms available

#### Test Case 5.2: Update Profile
**Steps:**
1. On profile page, modify:
   - First/Last name
   - Email
   - Phone
   - Bio
   - Role (optional)
2. Click "Update Profile"

**Expected Results:**
- Changes saved successfully
- Success message displayed
- Updated information visible
- Changes reflected in navigation

#### Test Case 5.3: View User's Properties
**Steps:**
1. Login as agent with properties
2. View profile page

**Expected Results:**
- "My Properties" section shows user's listings
- Shows property title, status, price
- Links to property detail
- Edit/Delete buttons for each property
- Shows property count

### 6. Admin Panel

#### Test Case 6.1: Admin Access
**Steps:**
1. Login as superuser
2. Navigate to /admin/

**Expected Results:**
- Admin panel loads
- All models visible: Users, Properties, Inquiries, Profiles
- Can manage all data

#### Test Case 6.2: Property Management in Admin
**Steps:**
1. In admin, navigate to Properties
2. View property list
3. Edit a property

**Expected Results:**
- List view shows key fields
- Filters available (status, type, city)
- Search works
- Can edit all fields
- Inline image management available

#### Test Case 6.3: Inquiry Management in Admin
**Steps:**
1. Navigate to Inquiries in admin
2. View inquiry list
3. Mark inquiries as read/unread

**Expected Results:**
- List view shows inquiries
- Can filter by read status
- Can search by property/user
- Can bulk mark as read/unread
- List editable for is_read field

## Test Scenarios

### Scenario 1: Complete Agent Workflow
1. Register as agent
2. Create 3 properties with different types
3. Upload images for properties
4. Receive inquiries from buyers
5. View and respond to inquiries
6. Edit property details
7. Mark property as sold
8. Delete a property

### Scenario 2: Complete Buyer Workflow
1. Register as buyer
2. Browse property listings
3. Use search and filters to find properties
4. View property details
5. Send inquiries about multiple properties
6. Track inquiry status
7. View inquiry responses
8. Update profile information

### Scenario 3: Multi-User Interaction
1. Agent creates properties
2. Buyer searches and filters
3. Buyer sends inquiries
4. Agent receives email notifications
5. Agent views inquiries in dashboard
6. Agent responds via email
7. Buyer checks inquiry status

## Browser Compatibility

Test on the following browsers:

- **Chrome** (latest version)
- **Firefox** (latest version)
- **Safari** (latest version)
- **Edge** (latest version)
- **Mobile browsers** (Chrome Mobile, Safari iOS)

**Test Points:**
- Layout and styling
- Form submissions
- Image uploads
- Navigation and links
- Responsive design
- JavaScript functionality

## Performance Testing

### Load Testing

1. **Create Test Data:**
   - 100+ properties
   - 50+ users
   - 200+ inquiries

2. **Test Scenarios:**
   - Property list page load time
   - Search/filter response time
   - Property detail page load
   - Image upload speed
   - Pagination performance

3. **Expected Performance:**
   - Page load: < 2 seconds
   - Search/filter: < 1 second
   - Image upload: < 5 seconds (depends on size)
   - Database queries: < 100ms

### Database Query Optimization

Check for N+1 query problems:
```python
from django.db import connection
from django.test.utils import override_settings

# Enable query logging
with override_settings(DEBUG=True):
    # Perform action
    print(len(connection.queries))  # Should be minimal
```

## Regression Testing

After any code changes, run:

1. Full automated test suite
2. Critical path manual tests:
   - User registration and login
   - Property creation
   - Search and filter
   - Inquiry submission
3. Visual regression (check UI consistency)

## Bug Reporting

When reporting bugs, include:

1. **Steps to reproduce**
2. **Expected behavior**
3. **Actual behavior**
4. **Screenshots** (if applicable)
5. **Browser and version**
6. **Error messages** (from console/terminal)
7. **User role** (agent/buyer/admin)

## Test Data Cleanup

After testing:

```bash
# Reset database
python manage.py flush

# Reload fixtures
python manage.py loaddata users profiles properties inquiries

# Or delete and recreate database
rm db.sqlite3
python manage.py migrate
python manage.py loaddata users profiles properties inquiries
```

---

**Testing Checklist:**

- [ ] All automated tests pass
- [ ] Manual test cases completed
- [ ] Browser compatibility verified
- [ ] Performance acceptable
- [ ] No console errors
- [ ] Responsive design works
- [ ] Email notifications working
- [ ] Image uploads functional
- [ ] Search and filters accurate
- [ ] Authentication secure
- [ ] Authorization enforced
- [ ] Admin panel accessible
- [ ] Documentation updated

**Test Status:** ✅ Ready for Production / ⚠️ Issues Found / ❌ Failed