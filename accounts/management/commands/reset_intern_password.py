from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Reset intern password for testing'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email of the user')
        parser.add_argument('--password', type=str, default='intern2024', help='New password')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.is_approved = True  # Ensure user is approved
            user.is_active = True    # Ensure user is active
            user.save()
            
            self.stdout.write(f"Password reset for {email}")
            self.stdout.write(f"  Role: {user.role}")
            self.stdout.write(f"  Is Approved: {user.is_approved}")
            self.stdout.write(f"  Is Active: {user.is_active}")
            self.stdout.write(f"  New Password: {password}")
            
            # Test password
            if user.check_password(password):
                self.stdout.write("✓ Password verification successful")
            else:
                self.stdout.write("✗ Password verification failed")
                
        except User.DoesNotExist:
            self.stdout.write(f"User with email {email} not found")
            
            # List available users
            self.stdout.write("\nAvailable users:")
            for u in User.objects.all():
                self.stdout.write(f"  - {u.email} ({u.role})")
