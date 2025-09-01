"""Configuration for Airtable automation system."""
import os
from dotenv import load_dotenv

load_dotenv()

# Airtable configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

# Table names
APPLICANTS_TABLE = "Applicants"
PERSONAL_DETAILS_TABLE = "Personal Details"
WORK_EXPERIENCE_TABLE = "Work Experience"
SALARY_PREFERENCES_TABLE = "Salary Preferences"
SHORTLISTED_LEADS_TABLE = "Shortlisted Leads"

# LLM configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "airtable-automation")

# Shortlisting criteria
TIER_1_COMPANIES = ["Google", "Meta", "OpenAI", "Microsoft", "Amazon", "Apple", "Netflix"]
ELIGIBLE_COUNTRIES = ["US", "USA", "United States", "Canada", "UK", "United Kingdom", "Germany", "India"]
MIN_EXPERIENCE_YEARS = 4
MAX_HOURLY_RATE = 100
MIN_AVAILABILITY_HOURS = 20

