"""
Database management and cleanup utility
"""
import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import db, Candidate, Document, DocumentRequest
from config import Config

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def show_stats(self):
        print("\n" + "=" * 60)
        print("  DATABASE STATISTICS")
        print("=" * 60)
        
        total_candidates = self.session.query(Candidate).count()
        completed = self.session.query(Candidate).filter_by(extraction_status='completed').count()
        failed = self.session.query(Candidate).filter_by(extraction_status='failed').count()
        pending = self.session.query(Candidate).filter_by(extraction_status='pending').count()
        
        total_docs = self.session.query(Document).count()
        total_requests = self.session.query(DocumentRequest).count()
        
        print(f"\nCandidates:")
        print(f"  Total: {total_candidates}")
        print(f"  Completed Extractions: {completed}")
        print(f"  Failed Extractions: {failed}")
        print(f"  Pending: {pending}")
        
        print(f"\nDocuments Submitted: {total_docs}")
        print(f"Document Requests Generated: {total_requests}")
        
        if failed > 0:
            print(f"\n⚠️  Failed Extractions:")
            failed_candidates = self.session.query(Candidate).filter_by(extraction_status='failed').all()
            for c in failed_candidates:
                print(f"  - ID: {c.id}, File: {c.resume_filename}, Created: {c.created_at}")
    
    def show_candidates(self, limit=10):
        print("\n" + "=" * 60)
        print(f"  RECENT CANDIDATES (Last {limit})")
        print("=" * 60)
        
        candidates = self.session.query(Candidate).order_by(Candidate.created_at.desc()).limit(limit).all()
        
        if not candidates:
            print("\nNo candidates found.")
            return
        
        for c in candidates:
            print(f"\nID: {c.id}")
            print(f"  Name: {c.name or 'N/A'}")
            print(f"  Email: {c.email or 'N/A'}")
            print(f"  Phone: {c.phone or 'N/A'}")
            print(f"  Company: {c.company or 'N/A'}")
            print(f"  Status: {c.extraction_status}")
            print(f"  Created: {c.created_at}")
    
    def show_duplicates(self):
        """Find potential duplicate candidates"""
        print("\n" + "=" * 60)
        print("  DUPLICATE DETECTION")
        print("=" * 60)
        
        email_dupes = self.session.query(
            Candidate.email, func.count(Candidate.id)
        ).filter(
            Candidate.email.isnot(None)
        ).group_by(
            Candidate.email
        ).having(
            func.count(Candidate.id) > 1
        ).all()
        
        if email_dupes:
            print("\n⚠️  Duplicate Emails Found:")
            for email, count in email_dupes:
                print(f"  {email}: {count} candidates")
        
        phone_dupes = self.session.query(
            Candidate.phone, func.count(Candidate.id)
        ).filter(
            Candidate.phone.isnot(None)
        ).group_by(
            Candidate.phone
        ).having(
            func.count(Candidate.id) > 1
        ).all()
        
        if phone_dupes:
            print("\n⚠️  Duplicate Phone Numbers Found:")
            for phone, count in phone_dupes:
                print(f"  {phone}: {count} candidates")
        
        if not email_dupes and not phone_dupes:
            print("\n✅ No duplicates found")
    
    def cleanup_orphaned_files(self):
        """Remove files that don't have database records"""
        print("\n" + "=" * 60)
        print("  ORPHANED FILES CLEANUP")
        print("=" * 60)
        
        upload_folder = Config.UPLOAD_FOLDER
        if not os.path.exists(upload_folder):
            print("\n✅ No upload folder found")
            return
        
        # Get all files (not directories)
        all_files = set()
        for item in os.listdir(upload_folder):
            item_path = os.path.join(upload_folder, item)
            if os.path.isfile(item_path):
                all_files.add(item)
        
        # Get all filenames from database
        db_files = set()
        candidates = self.session.query(Candidate).all()
        for c in candidates:
            if c.resume_filename:
                db_files.add(c.resume_filename)
        
        documents = self.session.query(Document).all()
        for d in documents:
            if d.filename:
                db_files.add(d.filename)
        
        # Find orphaned files
        orphaned = all_files - db_files
        
        if orphaned:
            print(f"\n⚠️  Found {len(orphaned)} orphaned files:")
            for filename in orphaned:
                print(f"  - {filename}")
            
            confirm = input("\nDelete these files? (yes/no): ")
            if confirm.lower() == 'yes':
                for filename in orphaned:
                    filepath = os.path.join(upload_folder, filename)
                    try:
                        os.remove(filepath)
                        print(f"  ✅ Deleted: {filename}")
                    except Exception as e:
                        print(f"  ❌ Could not delete {filename}: {e}")
        else:
            print("\n✅ No orphaned files found")
    
    def cleanup_failed_extractions(self):
        print("\n" + "=" * 60)
        print("  FAILED EXTRACTIONS CLEANUP")
        print("=" * 60)
        
        failed = self.session.query(Candidate).filter_by(extraction_status='failed').all()
        
        if not failed:
            print("\n✅ No failed extractions found")
            return
        
        print(f"\n⚠️  Found {len(failed)} failed extractions:")
        for c in failed:
            print(f"  - ID: {c.id}, File: {c.resume_filename}, Created: {c.created_at}")
        
        confirm = input("\nDelete these candidates? (yes/no): ")
        if confirm.lower() == 'yes':
            for c in failed:
                if c.resume_filename:
                    filepath = os.path.join(Config.UPLOAD_FOLDER, c.resume_filename)
                    if os.path.exists(filepath):
                        os.remove(filepath)
                
                self.session.delete(c)
            
            self.session.commit()
            print(f"  ✅ Deleted {len(failed)} candidates")
    
    def reset_database(self):
        """Drop and recreate all tables"""
        print("\n" + "=" * 60)
        print("  DATABASE RESET")
        print("=" * 60)
        
        confirm = input("\n⚠️  This will DELETE ALL DATA. Are you sure? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            return
        
        confirm2 = input("Type 'DELETE ALL DATA' to confirm: ")
        if confirm2 != 'DELETE ALL DATA':
            print("Cancelled.")
            return
        
        # Drop all tables
        db.metadata.drop_all(self.engine)
        print("  ✅ Dropped all tables")
        
        # Recreate tables
        db.metadata.create_all(self.engine)
        print("  ✅ Recreated tables")
        
        # Clean upload folder
        if os.path.exists(Config.UPLOAD_FOLDER):
            for filename in os.listdir(Config.UPLOAD_FOLDER):
                filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                try:
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                except Exception as e:
                    print(f"  ⚠️  Could not delete {filename}: {e}")
            print("  ✅ Cleaned upload folder")
    
    def close(self):
        """Close database connection"""
        self.session.close()

def print_menu():
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "DATABASE MANAGER" + " " * 27 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n1. Show Statistics")
    print("2. Show Recent Candidates")
    print("3. Check for Duplicates")
    print("4. Cleanup Orphaned Files")
    print("5. Cleanup Failed Extractions")
    print("6. Reset Database (DANGER)")
    print("0. Exit")
    print("\n" + "=" * 60)

def main():
    db = DatabaseManager()
    
    try:
        while True:
            print_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                db.show_stats()
            elif choice == '2':
                limit = input("How many candidates to show? (default 10): ").strip()
                limit = int(limit) if limit else 10
                db.show_candidates(limit)
            elif choice == '3':
                db.show_duplicates()
            elif choice == '4':
                db.cleanup_orphaned_files()
            elif choice == '5':
                db.cleanup_failed_extractions()
            elif choice == '6':
                db.reset_database()
            elif choice == '0':
                print("\nGoodbye!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
    
    finally:
        db.close()

if __name__ == "__main__":
    main()
