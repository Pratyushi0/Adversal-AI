from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Adversarial AI RAG Security"
    DEBUG: bool = True
    BERT_MODEL: str = "distilbert-base-uncased"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    DRIFT_THRESHOLD: float = 0.15
    INTEGRITY_THRESHOLD: float = 0.7
    MAX_QUERY_LENGTH: int = 512
    TOP_K_RETRIEVAL: int = 5

    class Config:
        env_file = ".env"

settings = Settings()
