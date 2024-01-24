import os

from settus import BaseSettings, Field, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", populate_by_name=True, keyvault_url=os.getenv(key="AZURE_KEY_VAULT_ENDPOINT")
    )

    api_allow_origins: list[str] = ["http://localhost:3002"]
    # TODO in a local environment without a key vault URL the following two variables should populate by name,
    # i.e. CHAT_PROMPT_TEMPLATE and OPENAI_API_KEY but this doesn't work.
    # As a workaround the local .env file variables must match the alias names
    # i.e. CHAT-PROMPT-TEMPLATE and OPENAI-API-KEY which are the names of the secrets in Azure key vault.
    # This is different from the other environment variable names which all use snake case.
    chat_prompt_template: str = Field(default="placeholder-value", alias="chat-prompt-template")
    chat_message_word_limit: int = 300
    openai_api_key: str = Field(default="placeholder-value", alias="openai-api-key")
    openai_model: str = "gpt-4"
    openai_embedding_model: str = "text-embedding-ada-002"
    qdrant_collection: str = "ees"
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333


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
