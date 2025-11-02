# Sample Data Fixtures

This directory contains sample data fixtures for demo and testing purposes.

## Fixtures Included

- `users.json` - 5 sample users (1 admin, 2 agents, 2 buyers)
- `profiles.json` - User profiles with roles and contact information
- `properties.json` - 15 diverse property listings
- `inquiries.json` - 10 sample inquiries from buyers to properties

## Loading Fixtures

**Load all fixtures in order:**
```bash
python manage.py loaddata users
python manage.py loaddata profiles
python manage.py loaddata properties
python manage.py loaddata inquiries
```

**Or load all at once:**
```bash
python manage.py loaddata users profiles properties inquiries
```

## Sample User Credentials

**Admin:**
- Username: `admin`
- Password: `admin123`
- Role: Agent (with superuser privileges)

**Agents:**
- Username: `john_agent` / Password: `agent123`
- Username: `sarah_agent` / Password: `agent123`

**Buyers:**
- Username: `mike_buyer` / Password: `buyer123`
- Username: `emma_buyer` / Password: `buyer123`

## What's Included

**Properties:**
- 15 properties across various cities (LA, NYC, Austin, Miami, Chicago, Seattle, etc.)
- Different property types: Houses, Apartments, Condos, Townhouses, Land, Commercial
- Price range: $200K - $1.25M
- Various statuses: Available, Sold, Pending
- Owned by john_agent and sarah_agent

**Inquiries:**
- 10 inquiries from buyers (mike_buyer and emma_buyer)
- Mix of read and unread inquiries
- Realistic inquiry messages
- Demonstrates the inquiry workflow

## Notes

- Fixtures should be loaded on a fresh database or after running migrations
- If you encounter errors, ensure migrations are up to date: `python manage.py migrate`
- Property images are not included in fixtures (featured_image will be null)
- You can add images through the admin panel or property edit forms
- Passwords are hashed for security
- To reset passwords: `python manage.py changepassword <username>`

## Creating Your Own Fixtures

To export current data as fixtures:
```bash
python manage.py dumpdata auth.user --indent 2 > fixtures/users.json
python manage.py dumpdata accounts.userprofile --indent 2 > fixtures/profiles.json
python manage.py dumpdata properties.property --indent 2 > fixtures/properties.json
python manage.py dumpdata properties.inquiry --indent 2 > fixtures/inquiries.json
```

## Troubleshooting

**IntegrityError on load:**
- Ensure you're loading fixtures in the correct order (users → profiles → properties → inquiries)
- Check that foreign key references match

**Duplicate key errors:**
- Clear the database: `python manage.py flush`
- Or delete db.sqlite3 and run migrations again

**Password issues:**
- Fixture passwords are hashed using Django's password hasher
- If login fails, reset password: `python manage.py changepassword <username>`