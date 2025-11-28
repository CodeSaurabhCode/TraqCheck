"""
Initialize database tables for TraqCheck
Run this script after setting up your PostgreSQL database
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db

def init_database():
    """Create all database tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Verify tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n📊 Created tables:")
        for table in tables:
            print(f"  - {table}")
        
        print("\n✨ Database initialization complete!")

if __name__ == "__main__":
    init_database()
