from .base import Settings


class ProdSettings(Settings):
    # 日志配置
    LOG_LEVEL: int = 40
