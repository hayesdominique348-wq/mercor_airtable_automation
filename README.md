# Airtable Multi-Table Form + JSON Automation System

This system provides an automated pipeline for collecting, processing, and evaluating contractor applications using Airtable as the database and Python scripts for automation.

## System Overview

The system consists of:
- Multi-table Airtable schema with linked relationships
- JSON compression/decompression for data portability
- Automated shortlisting based on configurable criteria
- LLM-powered evaluation and enrichment
- LangSmith integration for prompt management

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- Airtable account
- OpenAI API key
- LangSmith account and API key

### 2. Installation

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=your_base_id
OPENAI_API_KEY=your_openai_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=airtable-automation
```

### 4. Airtable Base Setup

Create a new Airtable base with the following tables:

#### Applicants Table (Parent)
- **Applicant ID** (Autonumber, Primary field)
- **Compressed JSON** (Long text)
- **Shortlist Status** (Single select: "Shortlisted", "Not Shortlisted")
- **LLM Summary** (Long text)
- **LLM Score** (Number, 1-10)
- **LLM Follow-Ups** (Long text)

#### Personal Details Table
- **Record ID** (Autonumber, Primary field)
- **Applicant ID** (Link to Applicants)
- **Full Name** (Single line text)
- **Email** (Email)
- **Location** (Single line text)
- **LinkedIn** (URL)

#### Work Experience Table
- **Record ID** (Autonumber, Primary field)
- **Applicant ID** (Link to Applicants)
- **Company** (Single line text)
- **Title** (Single line text)
- **Start** (Date)
- **End** (Date)
- **Technologies** (Single line text)

#### Salary Preferences Table
- **Record ID** (Autonumber, Primary field)
- **Applicant ID** (Link to Applicants)
- **Preferred Rate** (Number)
- **Minimum Rate** (Number)
- **Currency** (Single select: "USD", "EUR", "GBP")
- **Availability (hrs/wk)** (Number)

#### Shortlisted Leads Table
- **Record ID** (Autonumber, Primary field)
- **Applicant** (Link to Applicants)
- **Compressed JSON** (Long text)
- **Score Reason** (Long text)
- **Created At** (Date time)

### 5. LangSmith Setup

1. Log into LangSmith
2. Create a new prompt named `applicant-evaluation`
3. Use this template:

```
You are a recruiting analyst. Given this JSON applicant profile, do four things:
1. Provide a concise 75-word summary.
2. Rate overall candidate quality from 1-10 (higher is better).
3. List any data gaps or inconsistencies you notice.
4. Suggest up to three follow-up questions to clarify gaps.

Applicant JSON:
{applicant_json}

Return exactly in this format:
Summary: <text>
Score: <integer>
Issues: <comma-separated list or 'None'>
Follow-Ups: <bullet list>
```

## How Each Component Works

### 1. Data Collection Flow

Since Airtable forms can't write to multiple tables simultaneously, applicants submit three separate forms:

1. **Personal Details Form** - Collects name, email, location, LinkedIn
2. **Work Experience Form** - Can be submitted multiple times for different positions
3. **Salary Preferences Form** - Collects rate expectations and availability

Each form requires the Applicant ID to link records together.

### 2. JSON Compression (`compress_json.py`)

This script:
- Reads data from all linked tables for each applicant
- Combines into a single JSON structure
- Stores in the Compressed JSON field

Run with:
```bash
python compress_json.py
```

Example compressed JSON:
```json
{
  "personal": {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "location": "New York, USA",
    "linkedin": "https://linkedin.com/in/janedoe"
  },
  "experience": [
    {
      "company": "Google",
      "title": "Senior Software Engineer",
      "start": "2020-01-15",
      "end": "2023-06-30",
      "technologies": "Python, Go, Kubernetes"
    }
  ],
  "salary": {
    "rate": 90,
    "minimum_rate": 80,
    "currency": "USD",
    "availability": 30
  }
}
```

### 3. JSON Decompression (`decompress_json.py`)

This script reverses the compression:
- Reads Compressed JSON field
- Creates/updates records in child tables
- Maintains exact synchronization

Run with:
```bash
python decompress_json.py
```

### 4. Lead Shortlisting (`shortlist_leads.py`)

Evaluates candidates against these criteria:

| Criterion | Rule |
|-----------|------|
| Experience | >= 4 years total OR worked at Tier-1 company |
| Compensation | Preferred Rate <= $100/hr AND Availability >= 20 hrs/week |
| Location | In US, Canada, UK, Germany, or India |

Run with:
```bash
python shortlist_leads.py
```

Creates records in Shortlisted Leads table with detailed scoring reasons.

### 5. LLM Evaluation (`llm_evaluation.py`)

Uses OpenAI GPT-4 to:
- Summarize candidate profile (75 words)
- Assign quality score (1-10)
- Identify data gaps
- Suggest follow-up questions

Features:
- Prompts managed in LangSmith
- Retry logic with exponential backoff
- Token usage controls
- Tracing for debugging

Run with:
```bash
python llm_evaluation.py
```

## Customization Guide

### Modify Shortlist Criteria

Edit `config.py`:

```python
# Companies considered Tier-1
TIER_1_COMPANIES = ["Google", "Meta", "OpenAI", "Microsoft"]

# Eligible countries
ELIGIBLE_COUNTRIES = ["US", "Canada", "UK", "Germany", "India"]

# Experience requirements
MIN_EXPERIENCE_YEARS = 4

# Compensation limits
MAX_HOURLY_RATE = 100
MIN_AVAILABILITY_HOURS = 20
```

### Add New Evaluation Factors

1. Add fields to Airtable schema
2. Update compression logic in `compress_json.py`
3. Add evaluation logic in `shortlist_leads.py`

### Change LLM Provider

To use a different LLM:

1. Update `llm_evaluation.py` to use new provider's SDK
2. Modify prompt format if needed
3. Update LangSmith prompt accordingly

## Security Considerations

- Never commit `.env` file
- Use Airtable's built-in permissions
- Rotate API keys regularly
- Monitor LLM token usage
- Implement rate limiting for production

## Troubleshooting

### Common Issues

1. **"Invalid API key"** - Check `.env` file and API key validity
2. **"Table not found"** - Ensure table names match exactly
3. **"Rate limit exceeded"** - Add delays between API calls
4. **"JSON decode error"** - Validate Compressed JSON field content

### Debug Mode

Add logging to scripts:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Production Considerations

1. **Scaling**: Use Airtable webhooks instead of polling
2. **Error Handling**: Implement proper logging and alerting
3. **Data Validation**: Add schema validation for JSON
4. **Performance**: Cache Airtable data for repeated operations
5. **Monitoring**: Track script execution and success rates

## Support

For issues or questions:
1. Check Airtable API documentation
2. Review OpenAI/LangSmith docs
3. Enable debug logging
4. Test with small data sets first

