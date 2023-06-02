from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from service_backend.settings import config_database


engine = create_engine( config_database.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#### for connection pooling use this 
#pool_size = 5  # Adjust the pool size as per your application's needs
#engine = create_engine(DATABASE_URL, pool_size=pool_size, pool_pre_ping=True)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close