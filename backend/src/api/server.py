import uuid
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from backend.src.api.telemetry import setup_telemetry
from backend.src.graph.workflow import app as compliance_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Drishti - Hate Speech Analyzer")

# Creating FASTAPI Instance
api = FastAPI(
    title="Drishti - Analyser",
    description="API for Drishti Hate Speech Analyzer",
    version="1.0.0"
)

# Data Model
class AuditRequest(BaseModel):
    pass

class ComplianceIssue(BaseModel):
    pass

class AuditResponse(BaseModel):
    pass

