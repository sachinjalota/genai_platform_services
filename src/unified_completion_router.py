import opik
from fastapi import APIRouter, Header, HTTPException, status  
from fastapi.responses import JSONResponse  
from litellm import completion  
from src.unified_input import UnifiedCompletionRequest 
from src.default_prompts import DEFAULT_SYSTEM_PROMPT  
from src.config import BASE_API_KEY, BASE_API_URL, BASE_API_HEADERS  
from src.logging_config import Logger  
  
router = APIRouter()  
logger = Logger.create_logger("unified_completion")  
  
@router.post("/chat_completion")
@opik.track
async def unified_completion(  
    request: UnifiedCompletionRequest,  
    x_session_id: str = Header(...),  
    x_usecase_id: str = Header(...)  
):  
    if not x_session_id or not x_usecase_id:  
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Missing X-Session-ID or X-Usecase-ID headers")  
  
    try:  
        messages = [{"role": "system", "content": request.system_prompt or DEFAULT_SYSTEM_PROMPT},  
                    {"role": "user", "content": request.user_prompt}]  
          
        if request.image_url:  
            messages[1]["content"] = [  
                {"type": "text", "text": request.user_prompt},  
                {"type": "image_url", "image_url": {"url": request.image_url}}  
            ]  
  
        response = completion(  
            model=request.model_name,  
            messages=messages,  
            stream=request.stream,  
            api_key=BASE_API_KEY,  
            base_url=BASE_API_URL,  
            headers={**BASE_API_HEADERS, "X-Session-ID": x_session_id, "X-Usecase-ID": x_usecase_id}  
        )  
  
        logger.info(f"Completion response generated: {response}")  
  
        return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)  
  
    except Exception as e:  
        logger.error(f"Error occurred: {str(e)}")  
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file : {str(e)}")