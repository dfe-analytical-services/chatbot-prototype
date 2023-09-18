from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_embedding_model: str = "text-embedding-ada-002"
    qdrant_host: str = "localhost"
    qdrant_collection: str = "ees"
    qdrant_port: int = 6333
    url_chat_ui: str = "http://localhost:3002"

    class Config:
        env_file = "../../.env"


settings = Settings()

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
    "loggers": {"response_automater": {"handlers": ["console"], "level": "DEBUG", "propagate": False}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}

settings = Settings()