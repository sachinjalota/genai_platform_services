import json  
from litellm.types.utils import ModelResponse  
from datetime import datetime  
  
class CustomModelResponse(ModelResponse):  
    def __init__(self):  
        super().__init__()  
        self.created = datetime.fromtimestamp(int(self.created))  
  
    def __str__(self):  
        return json.dumps(self.__dict__, indent=4, default=str)  