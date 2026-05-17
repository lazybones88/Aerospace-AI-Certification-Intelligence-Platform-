from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AERO_CERT_")

    app_name: str = "Aerospace Certification Intelligence API"
    debug: bool = False
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "certgraph_dev"
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
