import pydantic
import json

class BaseMessage(pydantic.BaseModel):
    def serialize(self):
        return json.dumps({ key:val for key, val in self.__dict__.items() if not key.startswith("_") and not callable(val) })
    
    @classmethod
    def deserialize(cls, data):
        return cls(**json.loads(data))