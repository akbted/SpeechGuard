"""
Main Entry Point for Hate Speech Detection Engine.

Orchestrates the video compliance audit workflow:
1. Takes a YouTube video URL
2. Processes through Azure Video Indexer
3. Analyzes content for hate speech violations (Indian context)
4. Generates compliance report
"""

import uuid
import json
import logging

from dotenv import load_dotenv
load_dotenv(override=True)

from backend.src.graph.workflow import app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("compliance-engine")


def run_audit():
    """
    Runs a video compliance audit for hate speech detection.
    """
    
    # Generate unique session ID
    session_id = str(uuid.uuid4())
    logger.info(f"Starting Audit Session: {session_id}")

    # Initial state for the workflow
    initial_state = {
        "video_url": "https://youtu.be/YOUR_VIDEO_ID",  # Replace with actual URL
        "video_id": f"vid_{session_id[:8]}",
        "compliance_results": [],
        "errors": []
    }

    print("\n" + "=" * 60)
    print("HATE SPEECH DETECTION ENGINE - INDIAN CONTEXT")
    print("=" * 60)
    print(f"\n[INPUT]")
    print(f"Video URL: {initial_state['video_url']}")
    print(f"Session ID: {session_id}")

    try:
        # Execute the LangGraph workflow
        final_state = app.invoke(initial_state)
        
        print("\n" + "=" * 60)
        print("COMPLIANCE AUDIT REPORT")
        print("=" * 60)
        
        print(f"\nVideo ID:  {final_state.get('video_id')}")
        print(f"Status:    {final_state.get('final_report_status', 'UNKNOWN')}")
        
        # Display violations
        print("\n[VIOLATIONS DETECTED]")
        print("-" * 40)
        
        results = final_state.get('compliance_results', [])
        
        if results:
            for i, issue in enumerate(results, 1):
                print(f"\n#{i}")
                print(f"  Category:      {issue.get('category')}")
                print(f"  Sub-category:  {issue.get('sub_category', 'N/A')}")
                print(f"  Severity:      {issue.get('severity')}")
                print(f"  Target Group:  {issue.get('target_group', 'N/A')}")
                print(f"  Timestamp:     {issue.get('time_stamp', 'N/A')}")
                print(f"  Legal Ref:     {issue.get('legal_reference', 'N/A')}")
                print(f"  Description:   {issue.get('description')}")
                if issue.get('flagged_text'):
                    print(f"  Flagged Text:  \"{issue.get('flagged_text')}\"")
        else:
            print("No violations found. Content appears compliant.")

        # Display errors if any
        errors = final_state.get('errors', [])
        if errors:
            print("\n[ERRORS]")
            print("-" * 40)
            for error in errors:
                print(f"  - {error}")

        # Final summary
        print("\n[FINAL REPORT]")
        print("-" * 40)
        print(final_state.get('final_report', 'No report generated.'))
        
        print("\n" + "=" * 60)

    except Exception as e:
        logger.error(f"Workflow Execution Failed: {str(e)}")
        raise


if __name__ == "__main__":
    run_audit()
