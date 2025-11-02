from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_user_profile_auto_creation(self):
        """Test profile is created automatically when user is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile) # type: ignore

    def test_user_profile_default_role(self):
        """Test default role is BUYER"""
        self.assertEqual(self.user.profile.role, 'BUYER') # type: ignore

    def test_user_profile_str_method(self):
        """Test profile string representation"""
        expected_str = f"Profile for {self.user.username}"
        self.assertEqual(str(self.user.profile), expected_str) # type: ignore

    def test_is_agent_property(self):
        """Test is_agent property method"""
        self.assertFalse(self.user.profile.is_agent) # type: ignore
        self.user.profile.role = 'AGENT' # type: ignore
        self.user.profile.save() # type: ignore
        self.assertTrue(self.user.profile.is_agent) # type: ignore

    def test_is_buyer_property(self):
        """Test is_buyer property method"""
        self.assertTrue(self.user.profile.is_buyer) # pyright: ignore[reportAttributeAccessIssue]
        self.user.profile.role = 'AGENT' # type: ignore
        self.user.profile.save() # type: ignore
        self.assertFalse(self.user.profile.is_buyer) # type: ignore

    def test_user_profile_one_to_one_relationship(self):
        """Test one-to-one relationship between user and profile"""
        user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        self.assertNotEqual(self.user.profile, user2.profile) # type: ignore

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')

    def test_registration_view_get(self):
        """Test GET request shows registration form"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_registration_view_post_valid_data(self):
        """Test successful registration with valid data"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'BUYER'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'newuser') # type: ignore
        self.assertEqual(user.profile.role, 'BUYER') # type: ignore

    def test_registration_creates_profile(self):
        """Test profile is created with selected role"""
        data = {
            'username': 'newagent',
            'email': 'agent@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'AGENT'
        }
        self.client.post(self.register_url, data)
        user = User.objects.get(username='newagent')
        self.assertEqual(user.profile.role, 'AGENT') # type: ignore

    def test_registration_auto_login(self):
        """Test user is automatically logged in after registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'BUYER'
        }
        response = self.client.post(self.register_url, data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_registration_invalid_data(self):
        """Test form validation errors with invalid data"""
        data = {
            'username': '',  # Invalid: empty username
            'email': 'invalid-email',  # Invalid email format
            'password1': 'pass',  # Too short
            'password2': 'different',  # Doesn't match
            'role': 'INVALID'  # Invalid role
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertTrue(response.context['form'].errors)

class UserLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.login_url = reverse('accounts:login')

    def test_login_view_get(self):
        """Test GET request shows login form"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post_valid_credentials(self):
        """Test successful login with valid credentials"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_view_post_invalid_credentials(self):
        """Test failed login with invalid credentials"""
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertTrue(len(messages) > 0)

class UserLogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_logout_view(self):
        """Test successful logout"""
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

class UserProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.profile_url = reverse('accounts:profile')

    def test_profile_view_requires_authentication(self):
        """Test login required for profile access"""
        response = self.client.get(self.profile_url)
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={self.profile_url}"
        )

    def test_profile_view_get(self):
        """Test GET request shows profile page for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_profile_view_update(self):
        """Test profile update with valid data"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'phone': '555-0123',
            'bio': 'Updated bio'
        }
        response = self.client.post(self.profile_url, data, follow=True)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.profile.phone, '555-0123') # type: ignore
        messages = list(response.context['messages'])
        self.assertTrue(len(messages) > 0)

class AuthenticationIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_full_registration_to_property_creation_flow(self):
        """Test complete user journey from registration to property creation"""
        # Step 1: Register as agent
        register_data = {
            'username': 'newagent',
            'email': 'agent@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'AGENT'
        }
        response = self.client.post(reverse('accounts:register'), register_data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue(response.context['user'].profile.is_agent)

        # Step 2: Create property (requires Property model)
        property_data = {
            'title': 'Test Property',
            'description': 'Test description',
            'price': '500000.00',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'zipcode': '12345',
            'bedrooms': 3,
            'bathrooms': 2.0,
            'area': 2000,
            'property_type': 'HOUSE',
            'status': 'AVAILABLE'
        }
        response = self.client.post(reverse('properties:property_create'), property_data, follow=True)
        self.assertEqual(response.status_code, 200)
        # Additional assertions would depend on Property model implementation

    def test_role_based_functionality(self):
        """Test different capabilities for agents and buyers"""
        # Register as buyer
        self.client.post(reverse('accounts:register'), {
            'username': 'testbuyer',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'buyer@example.com',
            'role': 'BUYER'
        })
        
        # Attempt to access property creation (should fail)
        response = self.client.get(reverse('properties:property_create'))
        self.assertEqual(response.status_code, 403)  # Or 302 if redirecting

        # Log out and register as agent
        self.client.logout()
        self.client.post(reverse('accounts:register'), {
            'username': 'testagent',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'agent@example.com',
            'role': 'AGENT'
        })

        # Attempt to access property creation (should succeed)
        response = self.client.get(reverse('properties:property_create'))
        self.assertEqual(response.status_code, 200)