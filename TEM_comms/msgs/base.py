import pydantic


class BaseMessage(pydantic.BaseModel):
    model_config = dict(extra="forbid")

    def serialize(self):
        return self.model_dump_json()
    
    @classmethod
    def deserialize(cls, data):
        return cls.model_validate_json(data)
