"""Script to compress applicant data from multiple tables into a single JSON object."""
import json
from pyairtable import Table
from config import (
    AIRTABLE_API_KEY, AIRTABLE_BASE_ID,
    APPLICANTS_TABLE, PERSONAL_DETAILS_TABLE,
    WORK_EXPERIENCE_TABLE, SALARY_PREFERENCES_TABLE
)


def get_table(table_name):
    """Get Airtable table instance."""
    return Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, table_name)


def get_linked_records(table, applicant_id_field, applicant_id):
    """Get records from a table linked to a specific applicant."""
    formula = f"{{Applicant ID}} = '{applicant_id}'"
    return table.all(formula=formula)


def compress_applicant_data(applicant_id):
    """Compress data from multiple tables into a single JSON object."""
    # Get table instances
    personal_table = get_table(PERSONAL_DETAILS_TABLE)
    experience_table = get_table(WORK_EXPERIENCE_TABLE)
    salary_table = get_table(SALARY_PREFERENCES_TABLE)
    
    # Get personal details (one-to-one)
    personal_records = get_linked_records(personal_table, "Applicant ID", applicant_id)
    personal_data = {}
    if personal_records:
        fields = personal_records[0]['fields']
        personal_data = {
            "name": fields.get("Full Name", ""),
            "email": fields.get("Email", ""),
            "location": fields.get("Location", ""),
            "linkedin": fields.get("LinkedIn", "")
        }
    
    # Get work experience (one-to-many)
    experience_records = get_linked_records(experience_table, "Applicant ID", applicant_id)
    experience_data = []
    for record in experience_records:
        fields = record['fields']
        experience_data.append({
            "company": fields.get("Company", ""),
            "title": fields.get("Title", ""),
            "start": fields.get("Start", ""),
            "end": fields.get("End", ""),
            "technologies": fields.get("Technologies", "")
        })
    
    # Get salary preferences (one-to-one)
    salary_records = get_linked_records(salary_table, "Applicant ID", applicant_id)
    salary_data = {}
    if salary_records:
        fields = salary_records[0]['fields']
        salary_data = {
            "rate": fields.get("Preferred Rate", 0),
            "minimum_rate": fields.get("Minimum Rate", 0),
            "currency": fields.get("Currency", "USD"),
            "availability": fields.get("Availability (hrs/wk)", 0)
        }
    
    # Create compressed JSON
    compressed_json = {
        "personal": personal_data,
        "experience": experience_data,
        "salary": salary_data
    }
    
    return json.dumps(compressed_json, indent=2)


def update_applicant_compressed_json(applicant_record_id, compressed_json):
    """Update the Compressed JSON field in the Applicants table."""
    applicants_table = get_table(APPLICANTS_TABLE)
    applicants_table.update(applicant_record_id, {"Compressed JSON": compressed_json})
    print(f"Updated compressed JSON for applicant record {applicant_record_id}")


def compress_all_applicants():
    """Compress data for all applicants."""
    applicants_table = get_table(APPLICANTS_TABLE)
    applicants = applicants_table.all()
    
    for applicant in applicants:
        applicant_id = applicant['fields'].get('Applicant ID')
        if not applicant_id:
            print(f"Skipping applicant without ID: {applicant['id']}")
            continue
            
        print(f"Compressing data for applicant: {applicant_id}")
        compressed_json = compress_applicant_data(applicant_id)
        update_applicant_compressed_json(applicant['id'], compressed_json)


if __name__ == "__main__":
    print("Starting JSON compression for all applicants...")
    compress_all_applicants()
    print("Compression completed!")

