# Quick Start Guide

Get the Airtable automation system running in 15 minutes.

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Set Up Environment

Create `.env` file:
```
AIRTABLE_API_KEY=your_key_here
AIRTABLE_BASE_ID=your_base_id_here
OPENAI_API_KEY=your_openai_key_here
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_PROJECT=airtable-automation
```

## 3. Create Airtable Base

1. Go to Airtable and create a new base
2. Create these tables with exact names:
   - Applicants
   - Personal Details
   - Work Experience
   - Salary Preferences
   - Shortlisted Leads

3. Set up fields as described in README.md

## 4. Get Your Base ID

1. Go to https://airtable.com/api
2. Select your base
3. Copy the base ID (starts with "app")
4. Add to `.env` file

## 5. Create Sample Data (Optional)

```bash
python sample_data.py
```

## 6. Run Automation

Full pipeline:
```bash
python run_automation.py
```

Individual steps:
```bash
python run_automation.py compress    # JSON compression only
python run_automation.py shortlist   # Shortlisting only
python run_automation.py evaluate    # LLM evaluation only
```

## 7. Check Results

1. Open your Airtable base
2. Check Applicants table for:
   - Compressed JSON field
   - Shortlist Status
   - LLM Summary and Score
3. Check Shortlisted Leads table for qualified candidates

## Common Issues

**"API key not found"**
- Double-check `.env` file exists and has correct keys

**"Table not found"**
- Ensure table names match exactly (case-sensitive)

**"No applicants found"**
- Run `sample_data.py` to create test data
- Or manually add records to Airtable

## Next Steps

1. Read full README.md for detailed documentation
2. Set up LangSmith prompts (see LANGSMITH_SETUP.md)
3. Customize shortlisting criteria in `config.py`
4. Add real applicant data through Airtable forms

