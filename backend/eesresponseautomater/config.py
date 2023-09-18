from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_embedding_model: str = "text-embedding-ada-002"
    qdrant_collection: str = "ees"
    qdrant_port: int = 6333
    url_public_site: str = "http://localhost:3002"
    host: str = "localhost"

    class Config:
        env_file = "../../.env"


settings = Settings()
