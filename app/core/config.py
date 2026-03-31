import os

#os.getenv is for runtime configuration
class Settings:
    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME", "TaskForge API")
        self.APP_ENV = os.getenv("APP_ENV", "development")
        self.DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/taskforge")
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

settings = Settings() #instantiating
