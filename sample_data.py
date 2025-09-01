"""Script to create sample data in Airtable for testing."""
from pyairtable import Table
from config import (
    AIRTABLE_API_KEY, AIRTABLE_BASE_ID,
    APPLICANTS_TABLE, PERSONAL_DETAILS_TABLE,
    WORK_EXPERIENCE_TABLE, SALARY_PREFERENCES_TABLE
)


def get_table(table_name):
    """Get Airtable table instance."""
    return Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, table_name)


def create_sample_applicants():
    """Create sample applicant data for testing."""
    
    # Sample applicants data
    applicants_data = [
        {
            "id": "APP001",
            "personal": {
                "name": "John Smith",
                "email": "john.smith@email.com",
                "location": "San Francisco, USA",
                "linkedin": "https://linkedin.com/in/johnsmith"
            },
            "experience": [
                {
                    "company": "Google",
                    "title": "Senior Software Engineer",
                    "start": "2019-03-01",
                    "end": "2022-08-31",
                    "technologies": "Python, Go, Kubernetes"
                },
                {
                    "company": "Startup Inc",
                    "title": "Software Engineer",
                    "start": "2017-06-01",
                    "end": "2019-02-28",
                    "technologies": "JavaScript, React, Node.js"
                }
            ],
            "salary": {
                "rate": 95,
                "minimum_rate": 85,
                "currency": "USD",
                "availability": 25
            }
        },
        {
            "id": "APP002",
            "personal": {
                "name": "Sarah Johnson",
                "email": "sarah.j@email.com",
                "location": "London, UK",
                "linkedin": "https://linkedin.com/in/sarahjohnson"
            },
            "experience": [
                {
                    "company": "Small Tech Co",
                    "title": "Junior Developer",
                    "start": "2021-01-15",
                    "end": "2023-12-31",
                    "technologies": "Python, Django"
                }
            ],
            "salary": {
                "rate": 120,
                "minimum_rate": 110,
                "currency": "USD",
                "availability": 40
            }
        },
        {
            "id": "APP003",
            "personal": {
                "name": "Raj Patel",
                "email": "raj.patel@email.com",
                "location": "Mumbai, India",
                "linkedin": "https://linkedin.com/in/rajpatel"
            },
            "experience": [
                {
                    "company": "Meta",
                    "title": "Staff Engineer",
                    "start": "2020-07-01",
                    "end": "",
                    "technologies": "React, GraphQL, Python"
                }
            ],
            "salary": {
                "rate": 80,
                "minimum_rate": 70,
                "currency": "USD",
                "availability": 30
            }
        }
    ]
    
    # Get table instances
    applicants_table = get_table(APPLICANTS_TABLE)
    personal_table = get_table(PERSONAL_DETAILS_TABLE)
    experience_table = get_table(WORK_EXPERIENCE_TABLE)
    salary_table = get_table(SALARY_PREFERENCES_TABLE)
    
    for applicant_data in applicants_data:
        print(f"Creating applicant: {applicant_data['id']}")
        
        # Create parent applicant record
        applicant_record = applicants_table.create({
            "Applicant ID": applicant_data["id"]
        })
        
        # Create personal details
        personal_table.create({
            "Applicant ID": [applicant_record['id']],
            "Full Name": applicant_data["personal"]["name"],
            "Email": applicant_data["personal"]["email"],
            "Location": applicant_data["personal"]["location"],
            "LinkedIn": applicant_data["personal"]["linkedin"]
        })
        
        # Create work experience records
        for exp in applicant_data["experience"]:
            experience_table.create({
                "Applicant ID": [applicant_record['id']],
                "Company": exp["company"],
                "Title": exp["title"],
                "Start": exp["start"],
                "End": exp["end"] if exp["end"] else None,
                "Technologies": exp["technologies"]
            })
        
        # Create salary preferences
        salary_table.create({
            "Applicant ID": [applicant_record['id']],
            "Preferred Rate": applicant_data["salary"]["rate"],
            "Minimum Rate": applicant_data["salary"]["minimum_rate"],
            "Currency": applicant_data["salary"]["currency"],
            "Availability (hrs/wk)": applicant_data["salary"]["availability"]
        })
        
        print(f"Created all records for {applicant_data['id']}")


if __name__ == "__main__":
    print("Creating sample data in Airtable...")
    print("WARNING: This will create new records. Continue? (y/n)")
    
    response = input().lower()
    if response == 'y':
        create_sample_applicants()
        print("\nSample data created successfully!")
        print("You can now run the automation scripts to test the system.")
    else:
        print("Operation cancelled.")

