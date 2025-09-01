# LangSmith Setup Guide

This guide walks you through setting up LangSmith for prompt management in the Airtable automation system.

## Prerequisites

1. LangSmith account (sign up at https://smith.langchain.com)
2. LangSmith API key

## Step 1: Create API Key

1. Log into LangSmith
2. Go to Settings > API Keys
3. Create a new API key
4. Copy the key and add to your `.env` file:
   ```
   LANGSMITH_API_KEY=your_langsmith_api_key_here
   ```

## Step 2: Create Project

1. In LangSmith dashboard, click "New Project"
2. Name it "airtable-automation" (or update in `.env`)
3. Set as default project for easier tracking

## Step 3: Create Evaluation Prompt

1. Go to the Prompts section
2. Click "Create Prompt"
3. Name: `applicant-evaluation`
4. Type: Chat
5. Model: gpt-4 (or your preferred model)

### Prompt Template

Add the following as your prompt template:

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

### Variables

- Add variable: `applicant_json`
- Type: String
- Description: "JSON representation of applicant data"

## Step 4: Test the Prompt

1. Click "Test" in the prompt editor
2. Add sample JSON:
   ```json
   {
     "personal": {"name": "Test User", "location": "USA"},
     "experience": [{"company": "Google", "title": "SWE"}],
     "salary": {"rate": 90, "availability": 30}
   }
   ```
3. Run test to verify output format

## Step 5: Version Control

1. Save the prompt
2. Add version tag: "v1.0"
3. Set as default version

## Alternative Prompt Variations

### Detailed Technical Evaluation

```
You are a technical recruiting specialist. Analyze this applicant JSON and provide:

1. Technical Skills Assessment (50 words)
   - Evaluate technical depth based on companies and technologies
   - Identify strongest technical areas

2. Experience Quality Score (1-10)
   - Weight Tier-1 company experience higher
   - Consider career progression

3. Red Flags or Concerns
   - List any gaps, inconsistencies, or concerns
   - Note if critical information is missing

4. Interview Focus Areas (3 bullet points)
   - Suggest technical areas to probe deeper
   - Include behavioral questions if relevant

Applicant JSON:
{applicant_json}

Format your response as:
Technical Assessment: <text>
Experience Score: <number>
Concerns: <list or 'None identified'>
Interview Focus:
• <point 1>
• <point 2>
• <point 3>
```

### Quick Screening Prompt

```
Quickly screen this applicant JSON. In exactly 4 lines:
1. One-line summary (max 15 words)
2. Fit score: 1-10
3. Biggest concern (or "None")
4. Most important follow-up question

Applicant JSON:
{applicant_json}
```

## Monitoring and Debugging

### View Traces

1. Run the evaluation script
2. Go to LangSmith > Projects > airtable-automation
3. View individual traces for each evaluation
4. Check latency, token usage, and responses

### Add Feedback

In the code, feedback is automatically logged:
```python
trace.log_feedback(
    score=1.0,
    key="llm_response",
    value=result
)
```

### Custom Metrics

Add custom evaluation metrics:
```python
trace.log_feedback(
    score=llm_results["score"] / 10,  # Normalize to 0-1
    key="candidate_quality",
    value=f"Score: {llm_results['score']}"
)
```

## Troubleshooting

### "Prompt not found" Error

1. Verify prompt name matches exactly: `applicant-evaluation`
2. Check API key has read permissions
3. Ensure prompt is published/saved

### Rate Limiting

1. LangSmith has generous limits but monitor usage
2. Implement caching for identical evaluations
3. Use batch operations for multiple candidates

### Slow Response Times

1. Check model selection (gpt-3.5-turbo is faster)
2. Reduce max_tokens if appropriate
3. Consider async processing for bulk operations

## Best Practices

1. **Version Control**: Tag prompt versions when making changes
2. **A/B Testing**: Create variant prompts to compare results
3. **Monitoring**: Set up alerts for failed evaluations
4. **Documentation**: Document prompt changes and rationale
5. **Validation**: Regularly review LLM outputs for quality

## Next Steps

1. Run `python llm_evaluation.py` to test the integration
2. Monitor first few runs in LangSmith dashboard
3. Adjust prompt based on output quality
4. Set up automated monitoring for production use

