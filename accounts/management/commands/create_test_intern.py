from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a test intern user for debugging'

    def handle(self, *args, **options):
        email = 'test@intern.com'
        password = 'test123'
        
        # Delete existing test user if exists
        User.objects.filter(email=email).delete()
        
        # Create new test user
        user = User.objects.create_user(
            email=email,
            first_name='Test',
            last_name='Intern',
            role='intern',
            is_approved=True,
            is_active=True,
            password=password
        )
        
        self.stdout.write(f"✓ Created test intern user:")
        self.stdout.write(f"  Email: {email}")
        self.stdout.write(f"  Password: {password}")
        self.stdout.write(f"  Role: {user.role}")
        self.stdout.write(f"  Is Approved: {user.is_approved}")
        self.stdout.write(f"  Is Active: {user.is_active}")
        
        # Verify password works
        if user.check_password(password):
            self.stdout.write("✓ Password verification successful")
        else:
            self.stdout.write("✗ Password verification failed")
            
        self.stdout.write(f"\nYou can now test login with:")
        self.stdout.write(f"Email: {email}")
        self.stdout.write(f"Password: {password}")
