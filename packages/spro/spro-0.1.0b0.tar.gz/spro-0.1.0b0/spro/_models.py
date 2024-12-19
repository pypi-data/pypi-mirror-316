from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal


class SProRequest(BaseModel):
    prompt: str = Field(default="")
    mask_type: Optional[str] = Field(default="char")
    mask_character: Optional[str] = Field(default="*")
    entities: Optional[List[str]] = Field(default_factory=list)
    origin: Literal["API"] = "API"

    @field_validator("mask_type")
    def validate_mask_type(cls, v):
        if v not in ["char", "label", "CHAR", "LABEL","ENHANCED","enhanced"]:
            raise ValueError('mask_type must be either "char" , "label" or "enhanced"')
        return v.lower()

    @field_validator("mask_character")
    def validate_mask_character(cls, v):
        if v is not None and (len(v) != 1 or not v.isprintable()):
            raise ValueError("mask_character must be a single printable character")
        return v

    @field_validator("entities")
    def convert_entities_to_uppercase(cls, v):
        if v is not None:
            return [entity.upper() for entity in v]
        return v
