from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "CloudTrim FinOps Bot"
    ENVIRONMENT: str = "development"
    SLACK_WEBHOOK_URL: str = "mock"
    
    # AWS Güvenlik Yapılandırması (Local testler için, prod'da IAM Role kullanılacak)
    AWS_DEFAULT_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = "mock"
    AWS_SECRET_ACCESS_KEY: str = "mock"
    SLACK_WEBHOOK_URL: str = "mock" 
    
    # AI Yapılandırması
    OPENAI_API_KEY: str
    AI_MODEL_NAME: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()