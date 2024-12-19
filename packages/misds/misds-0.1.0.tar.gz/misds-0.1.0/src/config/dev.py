from .base import Settings


class DevSettings(Settings):
    APP_DEBUG: bool = True

    # 日志配置
    LOG_LEVEL: int = 10
