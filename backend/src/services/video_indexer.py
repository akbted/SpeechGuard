import os
import time
import logging
import httpx
import yt_dlp

from azure.identity import DefaultAzureCredential
from src.config.settings import settings

class VideoIndexerService:
    def __init__(self):
        self.ACCOUNT_ID = settings.AZURE_VI_ACCOUNT_ID
        self.LOCATION = settings.AZURE_VI_LOCATION
        self.SUBSCRIPTION_ID = settings.AZURE_SUBSCRIPTION_ID
        self.RESOURCE_GRP = settings.AZURE_RESOURCE_GROUP
        self.VI_NAME = settings.AZURE_VI_NAME
        self.credential = DefaultAzureCredential()

    def get_access_token(self):
        pass

    def get_account_token(self):
        pass

    def download_yt_video(self):
        pass

    def upload_video(self):
        pass

    def wait_for_processing(self):
        pass

    def extract_data(self):
        pass