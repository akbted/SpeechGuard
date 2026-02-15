import os 
import logging
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from backend.src.config.settings import settings


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name="Azure Insights")


def setup_telemetry():
    """
    Observability Framework setup with proper service identification.
    """

    insight_connection_string = settings.APPLICATION_INSIGHT_CONNECTION_STRING
    if not insight_connection_string:
        logger.error("Connection String Not Found!")
        return 
    
    resource = Resource.create({
        SERVICE_NAME: "Drishti-Compliance-Engine",
        SERVICE_VERSION: "1.0.0",
        "service.namespace": "hate-speech-detection",
        "service.instance.id": os.getenv("HOSTNAME", "local-instance"),
        "deployment.environment": os.getenv("ENVIRONMENT", "development")
    })
    
    # Azure Insight Configuration
    try:
        configure_azure_monitor(
            connection_string=insight_connection_string,
            resource=resource, 
            logger_name="Azure Insights"
        )
        logger.info("Azure Monitor Tracking Enabled & Connected!")
        logger.info(f"Service: Drishti-Compliance-Engine v1.0.0")
    
    except Exception as e:
        logger.error(f"Setting Azure Insight Failed: {str(e)}")
        return
