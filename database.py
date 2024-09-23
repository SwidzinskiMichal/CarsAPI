from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



# My SQL connector
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:newpassword@localhost/cardb"


# Select DB test or production
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



def get_db():
    db = SessionLocal()  
    try:
        yield db  
    finally:
        db.close()  