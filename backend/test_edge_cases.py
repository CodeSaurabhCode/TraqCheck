"""
Test script to validate edge case handling in the resume upload system
"""
import os
import sys
import requests
import json
from pathlib import Path

# Base API URL
API_URL = "http://127.0.0.1:5000/api"

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_duplicate_upload():
    """Test that uploading the same resume twice is rejected"""
    print_section("TEST 1: Duplicate Resume Upload")
    
    # Create a test resume file
    test_file = Path("test_resume.txt")
    test_file.write_text("""
    John Doe
    Email: john.doe@example.com
    Phone: +1-234-567-8900
    
    Professional Summary:
    Experienced software engineer with 5 years of experience.
    
    Skills:
    - Python
    - JavaScript
    - React
    - Flask
    
    Work Experience:
    Senior Software Engineer at TechCorp (2020-Present)
    - Developed web applications
    - Led team of 5 developers
    """)
    
    try:
        # First upload - should succeed
        with open(test_file, 'rb') as f:
            response = requests.post(
                f"{API_URL}/upload",
                files={'file': ('test_resume.txt', f, 'text/plain')}
            )
        
        print(f"\n1st Upload Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ First upload successful")
            candidate_id = response.json().get('id')
            
            # Second upload - should be rejected with 409
            with open(test_file, 'rb') as f:
                response2 = requests.post(
                    f"{API_URL}/upload",
                    files={'file': ('test_resume.txt', f, 'text/plain')}
                )
            
            print(f"\n2nd Upload Status: {response2.status_code}")
            print(f"Response: {response2.json()}")
            
            if response2.status_code == 409:
                print("✅ Duplicate correctly rejected with 409 Conflict")
            else:
                print("❌ FAILED: Duplicate should return 409, got", response2.status_code)
            
            # Cleanup
            requests.delete(f"{API_URL}/candidates/{candidate_id}")
        else:
            print("❌ FAILED: First upload should succeed")
    
    finally:
        test_file.unlink(missing_ok=True)

def test_empty_file():
    """Test that empty files are rejected"""
    print_section("TEST 2: Empty File Upload")
    
    test_file = Path("empty_resume.txt")
    test_file.write_text("")
    
    try:
        with open(test_file, 'rb') as f:
            response = requests.post(
                f"{API_URL}/upload",
                files={'file': ('empty_resume.txt', f, 'text/plain')}
            )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400 and "empty" in response.json().get('error', '').lower():
            print("✅ Empty file correctly rejected")
        else:
            print("❌ FAILED: Empty file should be rejected with 400")
    
    finally:
        test_file.unlink(missing_ok=True)

def test_invalid_content():
    """Test that files with insufficient content are rejected"""
    print_section("TEST 3: Invalid/Insufficient Content")
    
    test_file = Path("invalid_resume.txt")
    test_file.write_text("Hi")  # Too short
    
    try:
        with open(test_file, 'rb') as f:
            response = requests.post(
                f"{API_URL}/upload",
                files={'file': ('invalid_resume.txt', f, 'text/plain')}
            )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400 and "too short" in response.json().get('error', '').lower():
            print("✅ Invalid content correctly rejected")
        else:
            print("❌ FAILED: Invalid content should be rejected")
    
    finally:
        test_file.unlink(missing_ok=True)

def test_no_extractable_data():
    """Test that resumes with no extractable identifying data are rejected"""
    print_section("TEST 4: No Identifying Information")
    
    test_file = Path("no_data_resume.txt")
    test_file.write_text("""
    This is a very long resume with lots of text but absolutely no identifying
    information whatsoever. There is no name, no email address, and no phone number.
    It just contains random text to make it pass the minimum length requirement.
    More random text here. And even more. Keep going with the random text.
    This should be long enough now to pass the 50 character minimum.
    But it should still fail because there's no name, email, or phone.
    """)
    
    try:
        with open(test_file, 'rb') as f:
            response = requests.post(
                f"{API_URL}/upload",
                files={'file': ('no_data_resume.txt', f, 'text/plain')}
            )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400 and "identifying information" in response.json().get('error', '').lower():
            print("✅ Resume with no data correctly rejected")
        else:
            print("❌ FAILED: Resume without identifying info should be rejected")
    
    finally:
        test_file.unlink(missing_ok=True)

def test_large_file():
    """Test that files over 10MB are rejected"""
    print_section("TEST 5: File Size Limit")
    
    test_file = Path("large_resume.txt")
    # Create a file larger than 10MB
    large_content = "A" * (11 * 1024 * 1024)  # 11MB
    test_file.write_text(large_content)
    
    try:
        with open(test_file, 'rb') as f:
            response = requests.post(
                f"{API_URL}/upload",
                files={'file': ('large_resume.txt', f, 'text/plain')}
            )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400 and "too large" in response.json().get('error', '').lower():
            print("✅ Large file correctly rejected")
        else:
            print("❌ FAILED: File over 10MB should be rejected")
    
    finally:
        test_file.unlink(missing_ok=True)

def test_successful_workflow():
    """Test the complete successful workflow"""
    print_section("TEST 6: Successful Complete Workflow")
    
    test_file = Path("valid_resume.txt")
    test_file.write_text("""
    Jane Smith
    Email: jane.smith@example.com
    Phone: +1-987-654-3210
    
    Professional Summary:
    Data scientist with expertise in machine learning and Python.
    
    Skills:
    - Python
    - Machine Learning
    - TensorFlow
    - SQL
    
    Work Experience:
    Data Scientist at DataCorp (2019-Present)
    - Built ML models
    - Analyzed large datasets
    
    Education:
    Master of Science in Computer Science
    Stanford University, 2019
    """)
    
    try:
        # Upload
        with open(test_file, 'rb') as f:
            response = requests.post(
                f"{API_URL}/upload",
                files={'file': ('valid_resume.txt', f, 'text/plain')}
            )
        
        print(f"\nUpload Status: {response.status_code}")
        
        if response.status_code == 201:
            candidate_id = response.json().get('id')
            print(f"✅ Upload successful - Candidate ID: {candidate_id}")
            
            # Get candidate details
            get_response = requests.get(f"{API_URL}/candidates/{candidate_id}")
            print(f"\nGet Candidate Status: {get_response.status_code}")
            
            if get_response.status_code == 200:
                candidate = get_response.json()
                print(f"✅ Retrieved candidate: {candidate.get('name')}")
                print(f"   Email: {candidate.get('email')}")
                print(f"   Phone: {candidate.get('phone')}")
                print(f"   Extraction Status: {candidate.get('extraction_status')}")
            
            # Cleanup
            delete_response = requests.delete(f"{API_URL}/candidates/{candidate_id}")
            if delete_response.status_code == 200:
                print("✅ Cleanup successful")
        else:
            print("❌ FAILED: Valid resume should be accepted")
            print(f"Response: {response.json()}")
    
    finally:
        test_file.unlink(missing_ok=True)

def main():
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "EDGE CASE TEST SUITE" + " " * 23 + "║")
    print("╚" + "═" * 58 + "╝")
    
    # Check if server is running
    try:
        requests.get(API_URL.replace('/api', '/health'))
        print("\n✅ Server is running")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Server is not running!")
        print("Please start the server with: python app.py")
        return
    
    # Run all tests
    test_duplicate_upload()
    test_empty_file()
    test_invalid_content()
    test_no_extractable_data()
    test_large_file()
    test_successful_workflow()
    
    print("\n" + "=" * 60)
    print("  Test Suite Complete")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
