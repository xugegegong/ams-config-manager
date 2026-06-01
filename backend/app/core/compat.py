"""Pydantic v1/v2 compatibility layer."""
try:
    # Pydantic v2
    from pydantic import BaseModel as PydanticBaseModel, field_validator  # noqa
    from pydantic import ConfigDict

    class CompatBaseModel(PydanticBaseModel):
        model_config = ConfigDict(from_attributes=True)

    def model_to_dict(obj):
        return obj.model_dump()

except ImportError:
    # Pydantic v1
    from pydantic import BaseModel as PydanticBaseModel  # noqa

    class CompatBaseModel(PydanticBaseModel):
        class Config:
            orm_mode = True

    def model_to_dict(obj):
        return obj.dict()
