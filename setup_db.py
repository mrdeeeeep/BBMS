from app import app
from extensions import db
from models import User

def init_db():
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@bloodbank.com').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@bloodbank.com',
                user_type='admin'
            )
            admin.set_password('admin123')  # Set a secure password in production
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")

if __name__ == '__main__':
    init_db() 