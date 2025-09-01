"""Script to decompress JSON data back into normalized Airtable tables."""
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


def find_linked_record(table, applicant_id):
    """Find existing record linked to applicant."""
    formula = f"{{Applicant ID}} = '{applicant_id}'"
    records = table.all(formula=formula)
    return records[0] if records else None


def upsert_personal_details(applicant_id, applicant_record_id, personal_data):
    """Create or update personal details record."""
    personal_table = get_table(PERSONAL_DETAILS_TABLE)
    
    fields = {
        "Applicant ID": [applicant_record_id],  # Link to parent
        "Full Name": personal_data.get("name", ""),
        "Email": personal_data.get("email", ""),
        "Location": personal_data.get("location", ""),
        "LinkedIn": personal_data.get("linkedin", "")
    }
    
    existing = find_linked_record(personal_table, applicant_id)
    if existing:
        personal_table.update(existing['id'], fields)
        print(f"Updated personal details for {applicant_id}")
    else:
        personal_table.create(fields)
        print(f"Created personal details for {applicant_id}")


def upsert_work_experience(applicant_id, applicant_record_id, experience_data):
    """Create or update work experience records."""
    experience_table = get_table(WORK_EXPERIENCE_TABLE)
    
    # Delete existing records to ensure exact match with JSON
    existing_records = experience_table.all(formula=f"{{Applicant ID}} = '{applicant_id}'")
    for record in existing_records:
        experience_table.delete(record['id'])
    
    # Create new records from JSON
    for exp in experience_data:
        fields = {
            "Applicant ID": [applicant_record_id],  # Link to parent
            "Company": exp.get("company", ""),
            "Title": exp.get("title", ""),
            "Start": exp.get("start", ""),
            "End": exp.get("end", ""),
            "Technologies": exp.get("technologies", "")
        }
        experience_table.create(fields)
    
    print(f"Created {len(experience_data)} work experience records for {applicant_id}")


def upsert_salary_preferences(applicant_id, applicant_record_id, salary_data):
    """Create or update salary preferences record."""
    salary_table = get_table(SALARY_PREFERENCES_TABLE)
    
    fields = {
        "Applicant ID": [applicant_record_id],  # Link to parent
        "Preferred Rate": salary_data.get("rate", 0),
        "Minimum Rate": salary_data.get("minimum_rate", 0),
        "Currency": salary_data.get("currency", "USD"),
        "Availability (hrs/wk)": salary_data.get("availability", 0)
    }
    
    existing = find_linked_record(salary_table, applicant_id)
    if existing:
        salary_table.update(existing['id'], fields)
        print(f"Updated salary preferences for {applicant_id}")
    else:
        salary_table.create(fields)
        print(f"Created salary preferences for {applicant_id}")


def decompress_applicant(applicant_record):
    """Decompress JSON data for a single applicant."""
    applicant_id = applicant_record['fields'].get('Applicant ID')
    compressed_json = applicant_record['fields'].get('Compressed JSON')
    
    if not applicant_id or not compressed_json:
        print(f"Skipping applicant {applicant_record['id']} - missing ID or JSON")
        return
    
    try:
        data = json.loads(compressed_json)
    except json.JSONDecodeError:
        print(f"Invalid JSON for applicant {applicant_id}")
        return
    
    print(f"Decompressing data for applicant: {applicant_id}")
    
    # Upsert data into child tables
    if "personal" in data:
        upsert_personal_details(applicant_id, applicant_record['id'], data["personal"])
    
    if "experience" in data:
        upsert_work_experience(applicant_id, applicant_record['id'], data["experience"])
    
    if "salary" in data:
        upsert_salary_preferences(applicant_id, applicant_record['id'], data["salary"])


def decompress_all_applicants():
    """Decompress data for all applicants with compressed JSON."""
    applicants_table = get_table(APPLICANTS_TABLE)
    applicants = applicants_table.all()
    
    for applicant in applicants:
        if applicant['fields'].get('Compressed JSON'):
            decompress_applicant(applicant)


if __name__ == "__main__":
    print("Starting JSON decompression for all applicants...")
    decompress_all_applicants()
    print("Decompression completed!")

