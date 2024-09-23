from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import Optional

class CarSchema(BaseModel):
    id: Optional[int] = None
    brand: str
    model: str
    year_of_production: int

    # Production year validator
    @field_validator("year_of_production")
    def check_production_year(cls, year_of_production):
        current_year = datetime.now().year
        if year_of_production < 1800 or year_of_production > current_year:
            raise ValueError(f"Production year must be between 1800 and {current_year}")
        return year_of_production

    class Config:
        orm_mode = True


class RatingSchema(BaseModel):
    id: Optional[int] = None
    car_id: Optional[int] = None
    car_rating: int = Field(..., ge=1, le=5)
    
    # Rating limit validation
    @field_validator("car_rating")
    def check_production_year(cls, car_rating):
        if car_rating < 1 or car_rating > 5:
            raise ValueError(f"The rating range for the car is between 1 and 5")
        return car_rating
    
    class Config:
        orm_mode = True