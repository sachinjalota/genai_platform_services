from typing import Optional, List, TypeAlias, Literal
from pydantic import BaseModel, Field
from src.config import DEFAULT_COMPLETION_MODEL

ChatCompletionModality: TypeAlias = Literal["text", "audio"]
  
class ChatCompletionRequest(BaseModel):
    model_name: str = Field(default=DEFAULT_COMPLETION_MODEL)
    system_prompt: Optional[str] = None
    user_prompt: str = Field(min_length=5)
    auth_params: BaseModel
    temperature: Optional[float] = Field(0.5, ge=0.0, le=1.0, 
                                         description="Between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both")
    top_p: Optional[float] = Field(0.95, ge=0.0, le=1.0, 
                                   description="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or temperature but not both.")
    max_completion_tokens: Optional[int] = -1
    frequency_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, 
                                               description="Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.")
    presence_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, 
                                               description="Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.")
    
    modalities: Optional[List[ChatCompletionModality]] = ["text"]
    image_url: Optional[str] = None
    stream: bool = False
    # session_id: str = Field(None, description="Session ID for guardrails")
    # usecase_id: str = Field(None, description="Usecase ID for guardrails")