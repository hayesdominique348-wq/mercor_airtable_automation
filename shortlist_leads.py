"""Script to auto-shortlist promising candidates based on defined rules."""
import json
from datetime import datetime
from pyairtable import Table
from config import (
    AIRTABLE_API_KEY, AIRTABLE_BASE_ID,
    APPLICANTS_TABLE, SHORTLISTED_LEADS_TABLE,
    TIER_1_COMPANIES, ELIGIBLE_COUNTRIES,
    MIN_EXPERIENCE_YEARS, MAX_HOURLY_RATE, MIN_AVAILABILITY_HOURS
)


def get_table(table_name):
    """Get Airtable table instance."""
    return Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, table_name)


def parse_date(date_str):
    """Parse date string to datetime object."""
    if not date_str:
        return None
    try:
        # Try common date formats
        for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None
    except:
        return None


def calculate_total_experience(experience_list):
    """Calculate total years of experience from work history."""
    total_days = 0
    for exp in experience_list:
        start = parse_date(exp.get("start"))
        end = parse_date(exp.get("end")) or datetime.now()
        
        if start and end and end > start:
            total_days += (end - start).days
    
    return total_days / 365.25  # Convert to years


def has_tier1_experience(experience_list):
    """Check if candidate has worked at a Tier-1 company."""
    for exp in experience_list:
        company = exp.get("company", "").strip()
        if any(tier1.lower() in company.lower() for tier1 in TIER_1_COMPANIES):
            return True, company
    return False, None


def is_eligible_location(location):
    """Check if candidate is in an eligible country."""
    if not location:
        return False, "No location specified"
    
    location_lower = location.lower()
    for country in ELIGIBLE_COUNTRIES:
        if country.lower() in location_lower:
            return True, country
    
    return False, location


def evaluate_candidate(applicant_data):
    """Evaluate if candidate meets shortlisting criteria."""
    reasons = []
    meets_criteria = True
    
    # Parse compressed JSON
    try:
        data = json.loads(applicant_data.get("Compressed JSON", "{}"))
    except json.JSONDecodeError:
        return False, ["Invalid or missing compressed JSON"]
    
    # Check experience criteria
    experience = data.get("experience", [])
    total_years = calculate_total_experience(experience)
    has_tier1, tier1_company = has_tier1_experience(experience)
    
    if total_years >= MIN_EXPERIENCE_YEARS:
        reasons.append(f"Has {total_years:.1f} years of experience (>= {MIN_EXPERIENCE_YEARS} required)")
    elif has_tier1:
        reasons.append(f"Worked at Tier-1 company: {tier1_company}")
    else:
        meets_criteria = False
        reasons.append(f"Does not meet experience criteria: {total_years:.1f} years, no Tier-1 experience")
    
    # Check compensation criteria
    salary = data.get("salary", {})
    preferred_rate = salary.get("rate", float('inf'))
    availability = salary.get("availability", 0)
    
    if preferred_rate <= MAX_HOURLY_RATE and availability >= MIN_AVAILABILITY_HOURS:
        reasons.append(f"Compensation fit: ${preferred_rate}/hr <= ${MAX_HOURLY_RATE}/hr, {availability}hrs/wk >= {MIN_AVAILABILITY_HOURS}hrs/wk")
    else:
        meets_criteria = False
        if preferred_rate > MAX_HOURLY_RATE:
            reasons.append(f"Rate too high: ${preferred_rate}/hr > ${MAX_HOURLY_RATE}/hr")
        if availability < MIN_AVAILABILITY_HOURS:
            reasons.append(f"Availability too low: {availability}hrs/wk < {MIN_AVAILABILITY_HOURS}hrs/wk")
    
    # Check location criteria
    location = data.get("personal", {}).get("location", "")
    is_eligible, location_info = is_eligible_location(location)
    
    if is_eligible:
        reasons.append(f"Located in eligible country: {location_info}")
    else:
        meets_criteria = False
        reasons.append(f"Not in eligible location: {location_info}")
    
    return meets_criteria, reasons


def create_shortlist_record(applicant_record, reasons):
    """Create a record in the Shortlisted Leads table."""
    shortlist_table = get_table(SHORTLISTED_LEADS_TABLE)
    
    fields = {
        "Applicant": [applicant_record['id']],  # Link to Applicants table
        "Compressed JSON": applicant_record['fields'].get('Compressed JSON', ''),
        "Score Reason": " | ".join(reasons)
    }
    
    shortlist_table.create(fields)
    print(f"Created shortlist record for {applicant_record['fields'].get('Applicant ID')}")


def update_shortlist_status(applicant_record_id, status):
    """Update the Shortlist Status field in Applicants table."""
    applicants_table = get_table(APPLICANTS_TABLE)
    applicants_table.update(applicant_record_id, {"Shortlist Status": status})


def shortlist_candidates():
    """Evaluate all candidates and shortlist those who meet criteria."""
    applicants_table = get_table(APPLICANTS_TABLE)
    shortlist_table = get_table(SHORTLISTED_LEADS_TABLE)
    
    # Get all applicants with compressed JSON
    applicants = applicants_table.all()
    
    shortlisted_count = 0
    for applicant in applicants:
        applicant_id = applicant['fields'].get('Applicant ID')
        
        # Skip if no compressed JSON
        if not applicant['fields'].get('Compressed JSON'):
            print(f"Skipping {applicant_id} - no compressed JSON")
            continue
        
        # Skip if already shortlisted
        existing_shortlist = shortlist_table.all(
            formula=f"{{Applicant}} = '{applicant['id']}'"
        )
        if existing_shortlist:
            print(f"Skipping {applicant_id} - already shortlisted")
            continue
        
        # Evaluate candidate
        meets_criteria, reasons = evaluate_candidate(applicant['fields'])
        
        if meets_criteria:
            create_shortlist_record(applicant, reasons)
            update_shortlist_status(applicant['id'], "Shortlisted")
            shortlisted_count += 1
            print(f"Shortlisted {applicant_id}: {'; '.join(reasons)}")
        else:
            update_shortlist_status(applicant['id'], "Not Shortlisted")
            print(f"Not shortlisted {applicant_id}: {'; '.join(reasons)}")
    
    print(f"\nShortlisting completed! {shortlisted_count} candidates shortlisted.")


if __name__ == "__main__":
    print("Starting candidate shortlisting process...")
    shortlist_candidates()

