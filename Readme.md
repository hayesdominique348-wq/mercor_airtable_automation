# Quick Start Guide

## 1. Airtable Base Access
- **Database**: https://airtable.com/appCKy0n6zLw6vmOa/shre21c18ufxfUj7N/tblWLJ8QoaXZdLS7g/viwiW1rTpJzNS4Er7
- **Forms**: Use the 3 provided form links for data collection

## 2. Local Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env.example and configure api_keys.
AIRTABLE_API_KEY=AIRTABLE_API_KEY
AIRTABLE_BASE_ID=BASE_ID

OPENAI_API_KEY=YOUR_OPEN_AI_KEY

LANGSMITH_API_KEY=AIRTABLE_API_KEY
LANGSMITH_PROJECT=PROJECT_ID
```

## 3. Run Automation
```bash
# Full pipeline
python run_automation.py

# Individual steps
python run_automation.py compress
python run_automation.py shortlist  
python run_automation.py evaluate
```

## 4. Test with Sample Data
```bash
python sample_data.py
```

## 5. Key Features
- ✅ Multi-table form data collection
- ✅ JSON compression/decompression
- ✅ Automated shortlisting with configurable criteria
- ✅ LLM-powered candidate evaluation
- ✅ LangSmith integration for prompt management
- ✅ Comprehensive error handling and retry logic

## 6. Customization
Edit `config.py` to modify:
- Shortlisting criteria
- Tier-1 companies list
- Eligible countries
- Experience requirements