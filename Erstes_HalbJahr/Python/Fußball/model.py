from pydantic import BaseModel, Field, field_validator, ValidationError

class Spieler(BaseModel):
    name: str = Field(min_length=2, default="Franz")
    jahrgang: int = Field(default=2000)
    stearke: int = Field(ge=1, le=10, default=5)
    torschuss: int = Field(ge=1, le=10, default=5)
    motivation: int = Field(ge=1, le=10, default=5)

    model_config = {"validate_assignment": True}

s = Spieler(name="Eray", jahrgang=2007, stearke=10, torschuss=6, motivation=1)
print(s)
print(s.model_dump())
    