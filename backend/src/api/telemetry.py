import os 
import logging
from azure.monitor.opentelemetry import configure_azure_monitor
from backend.src.config.settings import settings

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name="Azure Insights")

def setup_telemetry():
    """
    Observability Framework setup.
    """

    insight_connection_string = settings.APPLICATION_INSIGHT_CONNECTION_STRING
    if not insight_connection_string:
        logger.error("Connection String Not Found!")
        return 
    
    # Azure Insight
    try:
        configure_azure_monitor(
            connection_string = insight_connection_string,
            logger_name = "Azure Insights"
        )
        logger.info(" Azure Monitor Tracking Enabled & Connected!")    
    
    except Exception as e:
        logger.error("Setting Azure Insight Failed")
        return 

