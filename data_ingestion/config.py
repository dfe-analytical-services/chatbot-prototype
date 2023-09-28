from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ees_url_api_content: str = "http://localhost:5010/api"
    ees_url_api_data: str = "http://localhost:5000/api"
    ees_url_public_ui: str = "http://localhost:3000"
    openai_api_key: str
    openai_embedding_model: str = "text-embedding-ada-002"
    qdrant_collection: str = "ees"
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333


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
    "loggers": {"data_ingestion": {"handlers": ["console"], "level": "DEBUG", "propagate": False}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}

settings = Settings()
