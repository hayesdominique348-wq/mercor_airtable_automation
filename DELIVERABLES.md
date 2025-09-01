# Airtable Multi-Table Form + JSON Automation - Deliverables

## 1. Airtable Base (Share Link)

**Public Database Link:** https://airtable.com/appCKy0n6zLw6vmOa/shre21c18ufxfUj7N/tblWLJ8QoaXZdLS7g/viwiW1rTpJzNS4Er7

**Form Links:**
- Applicant Registration Form: https://airtable.com/appCKy0n6zLw6vmOa/pagj2GIZwRcyCLHlS/form
- Personal Details Form: https://airtable.com/appCKy0n6zLw6vmOa/pagkY4nTYG9WJs7TO/form
- Work Experience Form: https://airtable.com/appCKy0n6zLw6vmOa/pagshFukJNZcNxAYq/form  
- Salary Preferences Form: https://airtable.com/appCKy0n6zLw6vmOa/pagX00w67OM5sJFuz/form

## 2. System Architecture

### Database Schema
The system uses 5 interconnected tables:

1. **Applicants** (Parent Table)
   - Applicant ID (Primary Key)
   - Compressed JSON (Long Text)
   - Shortlist Status (Single Select)
   - LLM Summary (Long Text)
   - LLM Score (Number 1-10)
   - LLM Follow-Ups (Long Text)

2. **Personal Details** (Child Table)
   - Record ID (Primary Key)
   - Applicant ID (Link to Applicants)
   - Full Name, Email, Location, LinkedIn

3. **Work Experience** (Child Table)
   - Record ID (Primary Key)
   - Applicant ID (Link to Applicants)
   - Company, Title, Start Date, End Date, Technologies

4. **Salary Preferences** (Child Table)
   - Record ID (Primary Key)
   - Applicant ID (Link to Applicants)
   - Preferred Rate, Minimum Rate, Currency, Availability

5. **Shortlisted Leads** (Results Table)
   - Record ID (Primary Key)
   - Applicant (Link to Applicants)
   - Compressed JSON (Long Text)
   - Score Reason (Long Text)
   - Created At (DateTime)

## 3. Automation Scripts

### Core Scripts
- `compress_json.py` - Compresses multi-table data into single JSON
- `decompress_json.py` - Reverses compression back to normalized tables
- `shortlist_leads.py` - Auto-shortlists candidates based on criteria
- `llm_evaluation.py` - LLM-powered candidate evaluation
- `run_automation.py` - Main orchestrator script

### Configuration
- `config.py` - Centralized configuration and criteria
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (API keys)

## 4. How Each Component Works

### Data Collection Flow
1. Applicants submit 3 separate forms (Personal, Experience, Salary)
2. Each form links to parent Applicant record via Applicant ID
3. Forms populate respective child tables with linked relationships

### JSON Compression Process
```python
# Example compressed JSON structure
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

### Shortlisting Criteria
- **Experience**: ≥4 years total OR worked at Tier-1 company (Google, Meta, OpenAI, Microsoft, Amazon, Apple, Netflix)
- **Compensation**: Preferred Rate ≤$100/hr AND Availability ≥20 hrs/week
- **Location**: US, Canada, UK, Germany, or India

### LLM Evaluation Features
- Uses OpenAI GPT-4 for candidate assessment
- LangSmith integration for prompt management and tracing
- Generates summary, score (1-10), and follow-up questions
- Retry logic with exponential backoff
- Token usage controls and error handling

## 5. Setup Instructions

### Prerequisites
- Python 3.8+
- Airtable account with API access
- OpenAI API key
- LangSmith account (optional but recommended)

### Installation
```bash
pip install -r requirements.txt
```

### Environment Setup
Rename  `.env.example` to `.env` and in `.env` file, replace "your_openai_api_key" with your own your_openai_api_key.
```
OPENAI_API_KEY=your_openai_api_key
```

### Running Automation
```bash
# Run full pipeline
python run_automation.py

# Run individual steps
python run_automation.py compress
python run_automation.py shortlist
python run_automation.py evaluate
```

## 6. Security & Configuration

### API Key Management
- All API keys stored in environment variables
- Never hardcoded in source code
- Supports Airtable's built-in permissions system

### LLM Integration
- Prompts managed in LangSmith for version control
- Configurable model parameters (temperature, max_tokens)
- Budget controls and usage monitoring
- Comprehensive error handling and retry logic

### Customization Options
Edit `config.py` to modify:
- Tier-1 company list
- Eligible countries
- Experience requirements
- Compensation limits
- Evaluation criteria

## 7. Production Considerations

### Scaling
- Use Airtable webhooks instead of polling for real-time updates
- Implement proper logging and monitoring
- Add data validation and schema checks
- Cache frequently accessed data

### Error Handling
- Comprehensive try-catch blocks
- Graceful degradation when APIs fail
- Detailed logging for debugging
- Manual review fallbacks

### Performance
- Batch operations where possible
- Rate limiting to respect API limits
- Efficient data structures and algorithms
- Background processing for large datasets

## 8. Testing & Validation

### Sample Data
Use `sample_data.py` to create test records:
```bash
python sample_data.py
```

### Validation Steps
1. Verify form submissions create linked records
2. Test JSON compression/decompression cycle
3. Validate shortlisting criteria logic
4. Confirm LLM evaluation outputs
5. Check error handling scenarios

## 9. Troubleshooting

### Common Issues
- **Invalid API key**: Check `.env` file and key validity
- **Table not found**: Ensure table names match exactly
- **Rate limit exceeded**: Add delays between API calls
- **JSON decode error**: Validate Compressed JSON field content

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 10. Extension Points

### Adding New Evaluation Factors
1. Add fields to Airtable schema
2. Update compression logic in `compress_json.py`
3. Add evaluation logic in `shortlist_leads.py`
4. Modify LLM prompts if needed

### Changing LLM Provider
1. Update `llm_evaluation.py` to use new provider's SDK
2. Modify prompt format if required
3. Update LangSmith configuration
4. Test with sample data

### Custom Shortlisting Rules
1. Edit criteria in `config.py`
2. Modify evaluation logic in `shortlist_leads.py`
3. Update documentation
4. Test with various candidate profiles

---

**Note**: This system provides a complete automation pipeline for contractor application processing, from data collection through LLM-powered evaluation and shortlisting. All components are modular and can be customized based on specific requirements.
