import os
import time
import logging
import httpx
import yt_dlp

from azure.identity import DefaultAzureCredential
from backend.src.config.settings import settings

logger = logging.getLogger("video-indexer")

class VideoIndexerService:
    def __init__(self):
        self.account_id = settings.AZURE_VI_ACCOUNT_ID
        self.location = settings.AZURE_VI_LOCATION
        self.subscription_id = settings.AZURE_SUBSCRIPTION_ID
        self.resource_group = settings.AZURE_RESOURCE_GROUP
        self.vi_name = settings.AZURE_VI_NAME
        self.credential = DefaultAzureCredential()

    def get_access_token(self) -> str:
        """Generates an ARM Access Token."""
        try:
            token_object = self.credential.get_token("https://management.azure.com/.default")
            return token_object.token
        except Exception as e:
            logger.error(f"Failed to get Azure Token: {e}")
            raise

    def get_account_token(self, arm_access_token: str) -> str:
        """Exchanges ARM token for Video Indexer Account Token."""
        url = (
            f"https://management.azure.com/subscriptions/{self.subscription_id}"
            f"/resourceGroups/{self.resource_group}"
            f"/providers/Microsoft.VideoIndexer/accounts/{self.vi_name}"
            f"/generateAccessToken?api-version=2024-01-01"
        )
        headers = {"Authorization": f"Bearer {arm_access_token}"}
        payload = {"permissionType": "Contributor", "scope": "Account"}
        
        response = httpx.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to get VI Account Token: {response.text}")
        return response.json().get("accessToken")

    def download(self, url: str, output_path: str = "temp_video.mp4") -> str:
        """Downloads a YouTube video to a local file."""
        logger.info(f"Downloading YouTube video: {url}")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
            'quiet': False,
            'no_warnings': False,
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            logger.info("Download complete.")
            return output_path
        except Exception as e:
            raise Exception(f"YouTube Download Failed: {str(e)}")

    def upload(self, video_path: str, video_name: str) -> str:
        """Uploads a LOCAL FILE to Azure Video Indexer."""
        arm_token = self.get_access_token()
        vi_token = self.get_account_token(arm_token)

        api_url = f"https://api.videoindexer.ai/{self.location}/Accounts/{self.account_id}/Videos"
        
        params = {
            "accessToken": vi_token,
            "name": video_name,
            'language': 'en-US',
            "privacy": "Private",
            "indexingPreset": "Default",
        }
        
        logger.info(f"Uploading file {video_path} to Azure...")

        
        with open(video_path, 'rb') as video_file:
            files = {'file': ('video.mp4', video_file, 'video/mp4')}
            response = httpx.post(api_url, params=params, files=files, timeout=300.0)
        
        if response.status_code != 200:
            raise Exception(f"Azure Upload Failed: {response.text}")
        
        video_id = response.json().get("id")

        logger.info(f"Video uploaded successfully!")
        logger.info(f"Video ID: {video_id}")
        logger.info(f"Account ID: {self.account_id}")
        logger.info(f"Location: {self.location}")
        logger.info(f"Portal URL: https://www.videoindexer.ai/accounts/{self.account_id}/videos/{video_id}")
        logger.info(f"Direct API URL: https://api.videoindexer.ai/{self.location}/Accounts/{self.account_id}/Videos/{video_id}/Index")
    
            
        return video_id

    def wait_for_processing(self, video_id: str) -> dict:
        """Polls status until complete."""
        logger.info(f"Waiting for video {video_id} to process...")
        
        while True:
            arm_token = self.get_access_token()
            vi_token = self.get_account_token(arm_token)
            
            url = f"https://api.videoindexer.ai/{self.location}/Accounts/{self.account_id}/Videos/{video_id}/Index"
            params = {"accessToken": vi_token}
            response = httpx.get(url, params=params)
            data = response.json()
            
            state = data.get("state")
            if state == "Processed":
                logger.info(f"Video {video_id} processing complete.")
                return data
            elif state == "Failed":
                raise Exception("Video Indexing Failed in Azure.")
            elif state == "Quarantined":
                raise Exception("Video Quarantined (Copyright/Content Policy Violation).")
            
            logger.info(f"Status: {state}... waiting 30s")
            time.sleep(30)

    # def extract_data(self, vi_json: dict) -> dict:
    #     """Parses the Video Indexer JSON into our State format."""
    #     transcript_lines = []
    #     for v in vi_json.get("videos", []):
    #         for insight in v.get("insights", {}).get("transcript", []):
    #             transcript_lines.append(insight.get("text", ""))
        
    #     ocr_lines = []
    #     for v in vi_json.get("videos", []):
    #         for insight in v.get("insights", {}).get("ocr", []):
    #             ocr_lines.append(insight.get("text", ""))
                
    #     return {
    #         "transcript": " ".join(transcript_lines),
    #         "ocr_text": ocr_lines,
    #         "video_meta_data": {
    #             "duration": vi_json.get("summarizedInsights", {}).get("duration", {}).get("seconds"),
    #             "platform": "youtube"
    #         }
    #     }

    def extract_data(self, vi_json: dict) -> dict:
        """Parses the Video Indexer JSON into our State format."""
        
        # DEBUG: Log the structure
        import json
        logger.info(f"Full JSON structure: {json.dumps(vi_json, indent=2)[:1000]}...") 
        
        transcript_lines = []
        
        # Check if 'videos' key exists
        if 'videos' in vi_json and len(vi_json['videos']) > 0:
            video = vi_json['videos'][0]
            insights = video.get('insights', {})
            
            logger.info(f"Available insights keys: {list(insights.keys())}")
            
            # Get transcript
            transcript_data = insights.get('transcript', [])
            logger.info(f"Transcript entries found: {len(transcript_data)}")
            
            for entry in transcript_data:
                text = entry.get('text', '')
                if text:
                    transcript_lines.append(text)
        
        # If no transcript in 'videos', try 'summarizedInsights'
        if not transcript_lines and 'summarizedInsights' in vi_json:
            summary_transcript = vi_json['summarizedInsights'].get('transcript', [])
            for entry in summary_transcript:
                text = entry.get('text', '')
                if text:
                    transcript_lines.append(text)
        
        transcript_text = " ".join(transcript_lines)
        logger.info(f"Final transcript length: {len(transcript_text)} characters")
        
        if not transcript_text:
            logger.warning("NO TRANSCRIPT EXTRACTED - Check video audio!")
        
        # Extract OCR
        ocr_lines = []
        if 'videos' in vi_json and len(vi_json['videos']) > 0:
            video = vi_json['videos'][0]
            insights = video.get('insights', {})
            for ocr_entry in insights.get('ocr', []):
                ocr_lines.append(ocr_entry.get('text', ''))
                
        return {
            "transcript": transcript_text,
            "ocr_text": ocr_lines,
            "video_meta_data": {
                "duration": vi_json.get('summarizedInsights', {}).get('duration', {}).get('seconds'),
                "platform": "youtube"
            }
        }
