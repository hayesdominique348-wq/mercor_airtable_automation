"""LLM-powered evaluation of applicants using LangSmith integration."""
import json
from datetime import datetime
from typing import Dict, Any, List
import openai
from langsmith import Client
from config import (
    AIRTABLE_API_KEY, AIRTABLE_BASE_ID, APPLICANTS_TABLE,
    OPENAI_API_KEY, LANGSMITH_API_KEY, LANGSMITH_PROJECT
)
from pyairtable import Table


def get_table(table_name: str):
    """Get Airtable table instance."""
    return Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, table_name)


def evaluate_applicant_with_llm(applicant_data: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate a single applicant using LLM."""
    try:
        # Parse compressed JSON
        compressed_data = applicant_data.get("Compressed JSON", "{}")
        data = json.loads(compressed_data)
        
        # Prepare prompt for LLM evaluation
        prompt = f"""
        Evaluate this applicant for a technical role:

        Experience: {data.get('experience', [])}
        Skills: {data.get('skills', [])}
        Education: {data.get('education', [])}
        Salary Preferences: {data.get('salary', {})}
        Personal Details: {data.get('personal', {})}

        Provide evaluation in this JSON format:
        {{
            "score": <1-10 rating>,
            "summary": "<2-3 sentence summary>",
            "follow_ups": "<specific questions to ask>",
            "strengths": ["<list of strengths>"],
            "concerns": ["<list of concerns>"]
        }}
        """
        
        # Initialize OpenAI client
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Make LLM call
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert technical recruiter evaluating candidates."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Parse LLM response
            llm_response = response.choices[0].message.content
            evaluation = json.loads(llm_response)
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Return a default evaluation if LLM fails
            evaluation = {
                "score": 5,
                "summary": "LLM evaluation failed - manual review required",
                "follow_ups": "Please review this candidate manually",
                "strengths": ["Manual review needed"],
                "concerns": ["LLM evaluation failed"]
            }
        
        # Log to LangSmith if configured
        if LANGSMITH_API_KEY:
            try:
                langsmith_client = Client(api_key=LANGSMITH_API_KEY)
                langsmith_client.log(
                    project_name=LANGSMITH_PROJECT,
                    name="applicant-evaluation",
                    inputs={"applicant_data": data, "prompt": prompt},
                    outputs={"evaluation": evaluation},
                    metadata={
                        "applicant_id": applicant_data.get("Applicant ID"),
                        "model": "gpt-4",
                        "timestamp": datetime.now().isoformat()
                    }
                )
            except Exception as e:
                print(f"Warning: LangSmith logging failed: {e}")
        
        return evaluation
        
    except Exception as e:
        print(f"Error evaluating applicant: {e}")
        return {
            "score": 0,
            "summary": f"Evaluation failed: {str(e)}",
            "follow_ups": "Please review manually",
            "strengths": [],
            "concerns": ["Evaluation error occurred"]
        }


def update_applicant_evaluation(applicant_record_id: str, evaluation: Dict[str, Any]):
    """Update applicant record with LLM evaluation results."""
    applicants_table = get_table(APPLICANTS_TABLE)
    
    fields = {
        "LLM Summary": evaluation.get("summary", ""),
        "LLM Score": evaluation.get("score", 0),
        "LLM Follow-Ups": evaluation.get("follow_ups", "")
    }
    
    applicants_table.update(applicant_record_id, fields)
    print(f"Updated evaluation for applicant {applicant_record_id}")


def evaluate_all_applicants():
    """Evaluate all applicants using LLM and update their records."""
    print("Starting LLM evaluation of all applicants...")
    
    applicants_table = get_table(APPLICANTS_TABLE)
    
    # Get all applicants
    applicants = applicants_table.all()
    
    if not applicants:
        print("No applicants found to evaluate.")
        return
    
    print(f"Found {len(applicants)} applicants to evaluate.")
    
    evaluated_count = 0
    for applicant in applicants:
        applicant_id = applicant['fields'].get('Applicant ID', 'Unknown')
        print(f"Evaluating applicant: {applicant_id}")
        
        # Skip if no compressed JSON
        if not applicant['fields'].get('Compressed JSON'):
            print(f"Skipping {applicant_id} - no compressed JSON")
            continue
        
        # Perform LLM evaluation
        evaluation = evaluate_applicant_with_llm(applicant['fields'])
        
        # Update applicant record
        update_applicant_evaluation(applicant['id'], evaluation)
        
        evaluated_count += 1
        print(f"Completed evaluation for {applicant_id} (Score: {evaluation.get('score', 'N/A')})")
    
    print(f"\nLLM evaluation complete! Evaluated {evaluated_count} applicants.")


if __name__ == "__main__":
    evaluate_all_applicants()
