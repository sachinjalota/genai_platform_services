from typing import Optional, List, TypeAlias, Literal
from pydantic import BaseModel, Field 
from src.config import DEFAULT_COMPLETION_MODEL 

ChatCompletionModality: TypeAlias = Literal["text", "audio"]
  
class UnifiedCompletionRequest(BaseModel):  
    model_name: str = Field(min_length=5, default=DEFAULT_COMPLETION_MODEL)  
    system_prompt: Optional[str] = None  
    user_prompt: str = Field(..., min_length=5) 
    auth_params: BaseModel
    temperature: Optional[float] = 1
    max_completion_tokens: Optional[int] = -1
    max_tokens: Optional[int] = -1 
    modalities: Optional[List[ChatCompletionModality]] = ["text"]
    image_url: str = Field(..., description='Must be base64 image')
    stream: bool = False  