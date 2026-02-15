import uuid
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from fastapi.middleware.cors import CORSMiddleware


from backend.src.api.telemetry import setup_telemetry
from backend.src.graph.workflow import app as compliance_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Drishti - Hate Speech Analyzer")

# Setting up telemetry
setup_telemetry()

# Creating FASTAPI Instance
api = FastAPI(
    title="Drishti - Analyser",
    description="API for Drishti Hate Speech Analyzer",
    version="1.0.0"
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Model
class AuditRequest(BaseModel):
    video_url : str

class ComplianceIssue(BaseModel):
    category: str
    description: str
    severity: str
    time_stamp: Optional[str]
    sub_category: Optional[str]
    target_group: Optional[str]
    flagged_text: Optional[str]
    legal_reference: Optional[str]

class AuditResponse(BaseModel):
    session_id: str         
    video_id: str           
    status: str              
    final_report: str
    compliance_results: List[ComplianceIssue]
    errors: List[str] = []  

# Model Entry
@api.post("/audit", response_model=AuditResponse)
def audit_video(request: AuditRequest):

    video_url = request.video_url

    # Generate a session_id
    session_id = str(uuid.uuid4())
    video_id = f"Vid{session_id[:8]}"

    logger.info(f"Created a session {video_id} - video url {video_url}")
    
    # Graph Input
    initial_state = {
        "video_url": video_url,  
        "video_id": video_id,
        "compliance_results": [],
        "errors": []
    }

    try:
        final_state = compliance_graph.invoke(initial_state)

        logger.info(f"Graph execution complete for {video_id}")

        return AuditResponse(
                session_id=str(session_id),
                video_id=final_state.get("video_id", video_id),
                
                status=final_state.get("final_report_status", "UNKNOWN"),
                final_report=final_state.get("final_report", "No report generated."),
                compliance_results=final_state.get("compliance_results", []),
                errors=final_state.get("errors", [])
            )
        
    except Exception as e:
        logger.error(f"Audit Failed: {str(e)}")  
        
        raise HTTPException(
            status_code=500, 
            detail=f"Workflow Execution Failed: {str(e)}"
        )



