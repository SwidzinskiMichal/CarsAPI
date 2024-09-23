from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Car(Base):
    __tablename__ = "Car"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(30))
    model = Column(String(70))
    year_of_production = Column(Integer)

class CarRating(Base):
    __tablename__ = "CarRating"
    
    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey(Car.id))
    car_rating = Column(Integer)