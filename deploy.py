#!/usr/bin/env python3
"""Deployment script for Airtable automation system."""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are met."""
    print("Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8+ required")
        return False
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("ERROR: .env file not found")
        print("Create .env file with your API keys:")
        print("AIRTABLE_API_KEY=your_key")
        print("AIRTABLE_BASE_ID=your_base_id")
        print("OPENAI_API_KEY=your_key")
        print("LANGSMITH_API_KEY=your_key")
        return False
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("ERROR: requirements.txt not found")
        return False
    
    print("✅ Requirements check passed")
    return True

def install_dependencies():
    """Install Python dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e}")
        return False

def test_connection():
    """Test API connections."""
    print("Testing API connections...")
    try:
        from config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, OPENAI_API_KEY
        
        if not all([AIRTABLE_API_KEY, AIRTABLE_BASE_ID, OPENAI_API_KEY]):
            print("ERROR: Missing required API keys in .env file")
            return False
        
        print("✅ API keys configured")
        return True
    except ImportError as e:
        print(f"ERROR: Configuration error: {e}")
        return False

def run_sample_test():
    """Run a sample test to verify everything works."""
    print("Running sample test...")
    try:
        # Test compression
        from compress_json import compress_all_applicants
        compress_all_applicants()
        print("✅ Compression test passed")
        
        # Test shortlisting
        from shortlist_leads import shortlist_candidates
        shortlist_candidates()
        print("✅ Shortlisting test passed")
        
        return True
    except Exception as e:
        print(f"ERROR: Sample test failed: {e}")
        return False

def main():
    """Main deployment function."""
    print("=" * 50)
    print("AIRTABLE AUTOMATION DEPLOYMENT")
    print("=" * 50)
    
    steps = [
        ("Checking requirements", check_requirements),
        ("Installing dependencies", install_dependencies),
        ("Testing connections", test_connection),
        ("Running sample test", run_sample_test)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"❌ Deployment failed at: {step_name}")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ DEPLOYMENT SUCCESSFUL!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Run: python run_automation.py")
    print("2. Check Airtable for results")
    print("3. Customize config.py as needed")

if __name__ == "__main__":
    main()
