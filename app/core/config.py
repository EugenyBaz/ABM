from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
        Конфигурация приложения.

        Загружает значения из переменных окружения и файла `.env`.
        Используется как единая точка доступа к настройкам
        backend и Telegram-бота.
        """
    # --- Database ---
    DATABASE_URL: str

    # --- Telegram ---
    BOT_TOKEN: str | None = None

    # --- SMTP ---
    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None

    # --- API ---
    API_URL: str | None = None

    # --- Email ---
    REPORT_EMAIL: str | None = None
    MARKETING_EMAIL_SUBJECT: str | None = None

    # --- Forward-to-email access control ---
    # Храним как строку из .env: "id1,id2,id3"
    ALLOWED_FORWARD_USERS: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
    )

    def get_allowed_forward_users(self) -> list[int]:
        """
        Возвращает список разрешённых Telegram user_id
        из переменной окружения ALLOWED_FORWARD_USERS
        """
        if not self.ALLOWED_FORWARD_USERS:
            return []
        return [int(x.strip()) for x in self.ALLOWED_FORWARD_USERS.split(",")]


settings = Settings()