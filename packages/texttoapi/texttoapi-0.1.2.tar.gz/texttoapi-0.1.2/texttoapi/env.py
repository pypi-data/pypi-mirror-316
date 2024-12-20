import os
import sys
import logging
from dotenv import load_dotenv
load_dotenv()

log_level = os.getenv("logLevel", "info")

llm_azure = (os.getenv("llmAzure", "False") == "True")
if llm_azure:
    api_version = os.getenv("llmAzureApiVersion")
    model=os.getenv("llmAzureModel")
    api_key = os.getenv("llmAzureApiKey")
    azure_endpoint = os.getenv("llmAzureEndpoint")
    data_limit = int(os.getenv("llmAzureDataLimit"))
llm_system_prompt = os.getenv("llmSystemPrompt")
trace_url = os.getenv("traceUrl")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(module)s.py %(message)s", handlers=[logging.FileHandler("chat_agent_cli.log")])
    
# Console logger.
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.INFO)
streamHandler.setFormatter(logging.Formatter("%(message)s"))
logging.getLogger().addHandler(streamHandler)
    
