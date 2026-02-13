import operator
from typing import TypedDict, List, Annotated,  Dict, Optional, Any

class ComplianceIssue(TypedDict):
    category: str  # e.g., "hate_speech", "communal_incitement", "caste_discrimination"
    description: str
    severity: str  # "low", "medium", "high", "critical"
    time_stamp: Optional[str]
 
    sub_category: Optional[str]  # e.g., "religious", "caste-based", "regional", "gender"
    target_group: Optional[str]  # Who is being targeted
    confidence_score: Optional[float]  # Model confidence (0-1)
    flagged_text: Optional[str]  # The actual problematic content
    legal_reference: Optional[str]  # Relevant Indian law (IPC 153A, 295A, SC/ST Act, etc.)



# Global State Shared thoughtout workflow
class VideoAuditState(TypedDict):
    # Input
    video_url: str
    video_id: str

    # Injestion 
    local_file_path: Optional[str]
    ocr_text: List[str]
    transcript: Optional[str]
    video_meta_data: Dict[str, Any]

    # Analysis Output
    compliance_results: Annotated[List[ComplianceIssue], operator.add]

    # Final Result
    final_report_status: str
    final_report: str

    # Error (System Observability)
    errors: Annotated[List[str], operator.add]


