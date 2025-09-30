#!/usr/bin/env python
"""
Database reset script for ElevatePro Internships
"""
import os
import sys
import django
import pymysql

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shaderl_internships.settings')
django.setup()

from django.conf import settings

def reset_database():
    """Reset the database by dropping and recreating it"""
    db_config = settings.DATABASES['default']
    
    print("🗄️  Resetting database...")
    print(f"   Database: {db_config['NAME']}")
    print(f"   Host: {db_config['HOST']}")
    print(f"   User: {db_config['USER']}")
    
    try:
        # Connect to MySQL server (not specific database)
        connection = pymysql.connect(
            host=db_config['HOST'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            port=int(db_config['PORT']),
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Drop database if exists
            print("   🗑️  Dropping existing database...")
            cursor.execute(f"DROP DATABASE IF EXISTS `{db_config['NAME']}`")
            
            # Create database
            print("   🆕 Creating new database...")
            cursor.execute(f"CREATE DATABASE `{db_config['NAME']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            
        connection.commit()
        connection.close()
        
        print("✅ Database reset successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database reset failed: {e}")
        return False

def main():
    print("🚀 ElevatePro Internships - Database Reset")
    print("=" * 50)
    
    # Confirm action
    response = input("⚠️  This will DELETE ALL DATA in the database. Continue? (y/N): ")
    if response.lower() != 'y':
        print("   Operation cancelled.")
        return
    
    # Reset database
    if not reset_database():
        return
    
    # Run migrations
    print("\n📝 Running migrations...")
    os.system("python manage.py migrate")
    
    print("\n🎉 Database reset completed!")
    print("Next steps:")
    print("1. Create superuser: python manage.py createsuperuser")
    print("2. Start server: python manage.py runserver")

if __name__ == "__main__":
    main()
