import openai, opik
from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import JSONResponse
# from litellm import completion
from src.completion_input import ChatCompletionRequest
from src.default_prompts import DEFAULT_SYSTEM_PROMPT
from src.config import BASE_API_KEY, BASE_API_URL, BASE_API_HEADERS
from src.logging_config import Logger
from src.api.utility.guardrails import scan_prompt, scan_output

router = APIRouter()
logger = Logger.create_logger("chat_completion")

@router.post("/chatcompletion")
# @opik.track
async def chatcompletion(
    request: ChatCompletionRequest, 
    x_session_id: str = Header(...), 
    x_usecase_id: str = Header(...)
    ):
    if not x_session_id or not x_usecase_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Missing X-Session-ID or X-Usecase-ID headers")
    
    try:
        # Run guardrails validation for user prompt
        guardrails_input_result = scan_prompt(
            prompt=request.user_prompt, session_id=x_session_id, usecase_id=x_usecase_id
        )
        if not guardrails_input_result.get("is_valid", False):
            return JSONResponse(
                content={
                    "error": "Input Guardrails validation failed",
                    "details": guardrails_input_result,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        messages = [{"role": "system", "content": request.system_prompt or DEFAULT_SYSTEM_PROMPT}, 
                    {"role": "user", "content": request.user_prompt}]
        
        if request.image_url:  
            messages[1]["content"] = [
                {"type": "text", "text": request.user_prompt}, 
                {"type": "image_url", "image_url": {"url": request.image_url}}
                ]
        
        client = openai.OpenAI(
            api_key = BASE_API_KEY, 
            base_url = BASE_API_URL
        )
        
        response = client.chat.completions.create(
            model=request.model_name, 
            messages=messages, 
            stream=request.stream, 
            # headers={"X-Session-ID": x_session_id, "X-Usecase-ID": x_usecase_id}
        )

        logger.info(f"Completion response generated: {response}")

        # Run guardrails validation for LLM output
        guardrails_output_result = scan_output(
            input_prompt=request.user_prompt,
            output=response.dict()["choices"][0]["message"]["content"],
            session_id=x_session_id,
            usecase_id=x_usecase_id,
        )
        if not guardrails_output_result.get("is_valid", False):
            return JSONResponse(
                content={
                    "error": "Output Guardrails validation failed",
                    "details": guardrails_output_result,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file : {str(e)}")