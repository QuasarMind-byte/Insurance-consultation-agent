
# 用 Pydantic 做配置加载
# pip install pydantic pydantic-settings

from pathlib import Path

from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

#   获取项目根目录
APP_ROOT = Path(__file__).resolve().parents[2]

class EnvSettings(BaseSettings):
    """环境变量配置类: 用于加载环境变量配置"""
    model_config = SettingsConfigDict(
        env_file=(APP_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore", # 忽略额外的环境变量
    )

class AppSettings(EnvSettings):
    """应用配置类: 用于加载应用配置"""
    name: str = Field(alias="APP_NAME")
    host: str = Field(alias="APP_HOST", default="127.0.0.1")
    port: int = Field(alias="APP_PORT", default=8000)
    debug: bool = Field(alias="APP_DEBUG", default=False, description="是否开启调试模式")


class DatabaseSettings(EnvSettings):
    """数据库配置类: 用于加载数据库配置"""
    host: str = Field(alias="DB_HOST", default="localhost")
    port: int = Field(alias="DB_PORT", default=5432)
    name: str = Field(alias="DB_NAME", default="insurance")
    username: str = Field(alias="DB_USER", default="insurance")
    password: str = Field(alias="DB_PASSWORD", default="123456")
    # 连接池
    echo: bool = Field(alias="DB_ECHO", default=False)
    pool_size: int = Field(alias="DB_POOL_SIZE", default=5)
    max_overflow: int = Field(alias="DB_MAX_OVERFLOW", default=10)
    pool_recycle: int = Field(alias="DB_POOL_RECYCLE", default=1800)

    @computed_field
    @property
    def url(self) -> str:
        # 拼接数据库连接 URL
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            path=self.name,
        ).encoded_string()


class LLMSettings(EnvSettings):
    """模型相关配置"""
    api_key: str = Field(alias="DEEPSEEK_API_KEY")
    chat_model: str = Field(alias="CHAT_MODEL", default="deepseek-v4-flash")


class LoggingSettings(EnvSettings):
    """日志相关配置"""
    level: str = Field(alias="LOGGING_LEVEL", default="INFO") # 可选值：DEBUG、INFO、WARNING、ERROR、CRITICAL

class Config(BaseSettings):
    """整合所有配置"""
    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

# 启动时初始化配置
settings = Config()





