"""Main script to run all automation steps in sequence."""
import sys
import time
from compress_json import compress_all_applicants
from shortlist_leads import shortlist_candidates
from llm_evaluation import evaluate_all_applicants


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60 + "\n")


def run_full_automation():
    """Run the complete automation pipeline."""
    print_header("AIRTABLE AUTOMATION PIPELINE")
    
    try:
        # Step 1: Compress JSON
        print_header("Step 1: JSON Compression")
        compress_all_applicants()
        time.sleep(2)  # Brief pause between steps
        
        # Step 2: Shortlist candidates
        print_header("Step 2: Lead Shortlisting")
        shortlist_candidates()
        time.sleep(2)
        
        # Step 3: LLM evaluation
        print_header("Step 3: LLM Evaluation")
        evaluate_all_applicants()
        
        print_header("AUTOMATION COMPLETE")
        print("All steps completed successfully!")
        
    except Exception as e:
        print(f"\nERROR: Automation failed - {e}")
        sys.exit(1)


def run_single_step(step):
    """Run a single automation step."""
    if step == "compress":
        print_header("Running JSON Compression")
        compress_all_applicants()
    elif step == "shortlist":
        print_header("Running Lead Shortlisting")
        shortlist_candidates()
    elif step == "evaluate":
        print_header("Running LLM Evaluation")
        evaluate_all_applicants()
    else:
        print(f"Unknown step: {step}")
        print("Valid steps: compress, shortlist, evaluate")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific step
        step = sys.argv[1].lower()
        run_single_step(step)
    else:
        # Run full automation
        run_full_automation()

