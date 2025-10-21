from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings (BaseSettings):
    """
    Application configuration settings.
    Loaded environment variables from '.env' with pydantic validation
    """

    #application
    app_name: str = "Social Blog API"
    api_version: str = "v1"
    debug: bool = True


    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()