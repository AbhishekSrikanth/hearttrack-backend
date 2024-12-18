#!/bin/sh

# Wait for the database to be ready
./wait-for-it.sh db:3306 -- echo "Database is ready!"

# Run migrations
python manage.py migrate

# Create admin user if it doesn't exist
echo "Checking if admin user exists..."
python manage.py shell << END
from users.models import CustomUser
if not CustomUser.objects.filter(username='admin').exists():
    CustomUser.objects.create_superuser('admin', 'admin@ht.com', 'admin')
    print("Admin user created!")
else:
    print("Admin user already exists.")
END

# Start the Django server
python manage.py runserver 0.0.0.0:8000
