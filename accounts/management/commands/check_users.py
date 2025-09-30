from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from applications.models import InternshipApplication

User = get_user_model()

class Command(BaseCommand):
    help = 'Check users and their status'

    def handle(self, *args, **options):
        self.stdout.write("=== USER STATUS CHECK ===")
        
        # Check all users
        users = User.objects.all()
        self.stdout.write(f"Total users: {users.count()}")
        
        for user in users:
            self.stdout.write(f"\nUser: {user.email}")
            self.stdout.write(f"  Role: {user.role}")
            self.stdout.write(f"  Is Approved: {user.is_approved}")
            self.stdout.write(f"  Is Active: {user.is_active}")
            self.stdout.write(f"  Is Superuser: {user.is_superuser}")
            
        # Check applications
        self.stdout.write("\n=== APPLICATIONS CHECK ===")
        applications = InternshipApplication.objects.all()
        self.stdout.write(f"Total applications: {applications.count()}")
        
        for app in applications:
            self.stdout.write(f"\nApplication: {app.email}")
            self.stdout.write(f"  Status: {app.status}")
            self.stdout.write(f"  Created Intern: {app.created_intern}")
            
        # Create test intern if none exists
        intern_users = User.objects.filter(role='intern')
        if not intern_users.exists():
            self.stdout.write("\n=== CREATING TEST INTERN ===")
            test_intern = User.objects.create_user(
                email='test.intern@example.com',
                first_name='Test',
                last_name='Intern',
                role='intern',
                is_approved=True,
                password='intern2024'
            )
            self.stdout.write(f"Created test intern: {test_intern.email}")
        else:
            self.stdout.write(f"\n=== EXISTING INTERNS ===")
            for intern in intern_users:
                self.stdout.write(f"Intern: {intern.email} (Approved: {intern.is_approved})")
