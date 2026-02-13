import json
import os
import logging
import re
from typing import Dict, Any, List
import logging

from src.graph.states import ComplianceIssue, VideoAuditState
from src.config.settings import settings, getLLMClient, getEmbedding, getVectorStore
from src.services.video_indexer import VideoIndexerService
from src.graph.prompt import setSystemPrompt
from langchain_core.messages import SystemMessage, HumanMessage

logger = logging.getLogger(name="compliance_engine")
logging.basicConfig(level=logging.INFO)


# Node 1
def index_video_node(state: VideoAuditState) -> Dict[str, Any]:
    """
    - Download YT Video
    - Upload to Azure Video Indexer (Blob Storage)
    - Extract Content
    """

    # Step 1: Get the YT URL and ID Link from state
    video_url = state.get("video_url", "")
    input_video_id = state.get("video_id", "demo")

    logger.info(f"Node 1 (Indexer) Processing {video_url}")

    # Step 2: Setting a local file name (temp download)
    local_file_name = "yt_temp_video.mp4"

    try:
        # Step 3: Creating an instance of Video Indexer Service
        vi_service = VideoIndexerService()

        # Step 4: Download the YT video to local path
        if "youtube.com" in video_url:
            local_path = vi_service.download(video_url, output_path=local_file_name)
        else:
            raise Exception("Please provide a valid URL")
        
        # Step 5: Upload the video to Azure Video Indexer
        azure_video_id = vi_service.upload(local_path, video_name=input_video_id)

        logger.info(f"Node 1 (Indexer) Upload Successful {video_url} to Azure - {azure_video_id}")

        # Step 5: Clean up the local storage
        if os.path.exists(local_path):
            os.remove(local_path)

        # Step 6: Get insights / extraction from VideoIndexer
        raw_insights = vi_service.wait_for_processing(azure_video_id)

        # Step 7: Cleaning the data
        clean_data = vi_service.extract_data(raw_insights)

        logger.info(f"Node 1 (Indexer) VideoIndexer Extraction Successful {video_url} to Azure - {azure_video_id}")

        return clean_data
    
    except Exception as e:
        logger.error(f"Node 1 (Indexer) VideoIndexer Failed {video_url}")
        return {
            "error" : str[e],
            "final_report_status": "Fail",
            "transcript": "",
            "ocr_text": []
        }



# Node 2
def compliance_auditor(state: VideoAuditState)-> Dict[str, Any]:
    """
    - Perform RAG to audit the given content of the Video
    - Builds a compliance report
    """

    logger.info("Compliance Auditor Running - Querying using Knowledge base and LLM")

    # Step 1: Get the transcript the state
    transcript = state.get("transcripts", "")
    if not transcript:
        logger.warning("Transcript not found, Skipping Audit")
        return {
            "final_report_status": "FAIL",
            "final_report" : "Audit skipped because video processing failed (No Transcript)"
        }
    
    # Step 2: Intialize the LLM Client
    llm = getLLMClient()

    # Step 3: Intialize the Embedding Client
    embedding = getEmbedding()

    # Step 4: Intalize the Vector Store
    vector_store = getVectorStore()

    # Step5: RAG (Implmentation)
    # Step5.5 Get OCR text from the state
    ocr_text = state.get("ocr_text", [])

    # Step5.6 Combine Transcript and OCR
    query_text = f"{transcript} {' '.join(ocr_text)}"

    # Step5.7 - Similarity Search
    docs = vector_store.similarity_search(query_text, k=5)

    # Step5.8 - Combine the retrived information
    retrieved_rules = "\n\n".join([doc.page_content for doc in docs])

    # Step 6 - System Prompt for the LLM (Role of the LLM)
    system_prompt = setSystemPrompt(retrieved_rules)

    # Step 7 - Set User Input
    user_message = f"""
    VIDEO METADATA: {state.get('video_meta_data', {})}
    TRANSCRIPT: {transcript}
    ON-SCREEN TEXT (OCR): {ocr_text}
    """

    # Step 8 - Invoking the LLM with System prompt and UserMessage
    try: 
        response = llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
        )

        # Step 9 - Cleaning the output of LLM 
        content = response.content
        if "```" in content:
            # Regex to find JSON inside code blocks
            content = re.search(r"```(?:json)?(.*?)```", content, re.DOTALL).group(1)

        audit_data = json.loads(content.strip())

        return {
            "compliance_results": [
                ComplianceIssue(
                    category=issue.get("category", "Unknown"),
                    sub_category=issue.get("sub_category"),
                    severity=issue.get("severity", "MEDIUM"),
                    description=issue.get("description", ""),
                    flagged_text=issue.get("flagged_text"),
                    time_stamp=issue.get("time_stamp"),
                    target_group=issue.get("target_group"),
                    legal_reference=issue.get("legal_reference")
                )
                for issue in audit_data.get("compliance_results", [])
            ],
            "final_report_status": audit_data.get("status", "FAIL"),
            "final_report": audit_data.get("final_report", "No report generated.")
        }

    except Exception as e:
        logger.error(f"System Error in Auditor Node: {str(e)}")
        # Log the raw response to see what went wrong
        logger.error(f"Raw LLM Response: {response.content if 'response' in locals() else 'None'}")
        return {
            "errors": [str(e)],
            "final_report_status": "FAIL"
        }