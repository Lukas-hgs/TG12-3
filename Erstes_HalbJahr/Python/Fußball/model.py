from pydantic import BaseModel, Field, field_validator, ValidationError

class Spieler(BaseModel):
    name: str = Field(min_length=2, default="Franz")
    jahrgang: int = Field( default=2000)
    stearke: int = Field(ge=1, le=10, default=5)
    torschuss: int = Field(ge=1, le=10, default=5)
    motivation: int = Field(ge=1, le=10, default=5)

    model_config = {"validate_assignment": True}

s1 = Spieler(name="Eray", jahrgang=2007, stearke=6, torschuss=8, motivation=1)
s2 = Spieler(name="Lena", jahrgang=2005, stearke=7, torschuss=8, motivation=9)


print(s1)
print(s1.model_dump())

print(s2)
print(s2.model_dump())
    