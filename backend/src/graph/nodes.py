import json
import os
import logging
import re
from typing import Dict, Any, List
import logging

from src.graph.states import ComplianceIssue, VideoAuditState
from src.config.settings import settings
from src.services.video_indexer import VideoIndexerService

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
        logger.info(f"Node 1 (Indexer) VideoIndexer Failed {video_url}")
        return {
            "error" : str[e],
            "final_report_status": "Fail",
            "transcript": "",
            "ocr_text": []
        }




