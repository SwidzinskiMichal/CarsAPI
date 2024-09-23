from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Car, Base, CarRating
from schemas import CarSchema, RatingSchema
from typing import List


app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Tables Created Successfully"}

# Post car to database
@app.post("/cars/", response_model=CarSchema)
def create_car(car: CarSchema, db: Session = Depends(get_db)):
    new_car = Car(
                  brand=car.brand,
                  model=car.model,
                  year_of_production=car.year_of_production
                 )
    
    db.add(new_car)
    db.commit()  
    db.refresh(new_car)
    return new_car

# Post car rating to database
@app.post("/cars/{car_id}/rate/", response_model=RatingSchema)
def create_car(car_id: int, rating_data: RatingSchema, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail=f"Car with id {car_id} does not exist")
    
    new_rating = CarRating(
                            car_id=car_id,
                            car_rating=rating_data.car_rating
                          )
    
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

# View top 10 rated cars
@app.get("/cars/top10", response_model=List[CarSchema])
def read_top_cars(db: Session = Depends(get_db)):
    top_cars = (
        db.query(Car, func.avg(CarRating.car_rating).label('average_rating'))
        .join(CarRating, Car.id == CarRating.car_id)
        .group_by(Car.id)
        .order_by(func.avg(CarRating.car_rating).desc())
        .limit(10)
        .all()
    )

    cars = [car for car, avg_rating in top_cars]
    return cars
