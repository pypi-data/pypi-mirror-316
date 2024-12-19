import os
from functools import lru_cache
from typing import Union

from .dev import DevSettings
from .prod import ProdSettings

__all__ = ["settings"]


@lru_cache()
def get_settings(
        env: str = os.getenv("ENV") or "dev",
) -> Union[DevSettings, ProdSettings]:
    """
    lru_cache ：只创建一次settings, 第一次会被调用。 使用函数不会被全局修改
    :param env: 环境变量配置
    :return:
    """

    env_config = {
        "dev": DevSettings,
        "prod": ProdSettings,
    }
    return env_config[env]()


settings = get_settings(os.getenv("ENV") or "dev")
