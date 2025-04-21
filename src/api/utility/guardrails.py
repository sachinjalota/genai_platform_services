import requests
import json
import src.config as config
from src.logging_config import Logger

logger = Logger.create_logger(__name__)

def scan_prompt(prompt: str, session_id: str, usecase_id: str) -> dict:
    headers = {
        "X-Session-ID": session_id,
        "X-Usecase-ID": usecase_id,
        "Content-Type": "application/json",
    }
    data = {
        "guardrail_id": config.INPUT_PROMPT_GUARDRAIL_ID,
        "prompt": prompt,
    }
    try:
        response = requests.post(config.GUARD_RAILS_INPUT_PROMPT_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error scanning prompt via guardrails: {str(e)}")
        return {"is_valid": False, "error": str(e)}

def scan_output(input_prompt: str, output: str, session_id: str, usecase_id: str) -> dict:
    headers = {
        "X-Session-ID": session_id,
        "X-Usecase-ID": usecase_id,
        "Content-Type": "application/json",
    }
    data = {
        "guardrail_id": config.OUTPUT_GUARDRAIL_ID,
        "prompt": input_prompt,
        "output": output,
    }
    try:
        response = requests.post(config.GUARD_RAILS_OUTPUT_PROMPT_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error scanning output via guardrails: {str(e)}")
        return {"is_valid": False, "error": str(e)}