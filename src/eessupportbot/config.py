from pydantic import BaseSettings


class Settings(BaseSettings):
    embedding_model: str = "text-embedding-ada-002"
    qdrant_collection: str = "ees"
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    url_api_content: str = "http://localhost:5010/api"
    url_api_data: str = "http://localhost:5000/api"
    url_public_site: str = "http://localhost:3000"

    # TODO update to use SettingsConfigDict from pydantic-settings once langchain is updated to use pydantic v2
    # model_config = SettingsConfigDict(env_file=".env")

    class Config:
        env_file = "../.env"


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "fmt": "%(levelprefix)s | %(asctime)s | %(name)s | %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",  # The default is stderr
        }
    },
    "loggers": {"eessupportbot": {"handlers": ["console"], "level": "DEBUG", "propagate": False}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}

settings = Settings()
