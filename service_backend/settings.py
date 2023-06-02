from dotenv import dotenv_values
# Load the environment variables from .env file
env_vars = dotenv_values()


class config_jwt():
    SECRET_KEY = "615b0a089a03cc0352371d25458d8631b3990cf9b0408bd711905dea8df9d6c5"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 5
    ALLOWED_DOMAINS = env_vars["ALLOWED_DOMAINS"].split(",")
    
class config_database():
    SQLALCHEMY_DATABASE_URL = "sqlite:///gotg.db"    
    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

class config_global():
    HOST = env_vars["BACKEND_HOST"]
    PROTOCOL = env_vars["BACKEND_PROTOCOL"]
    PORT = env_vars["BACKEND_PORT"]


