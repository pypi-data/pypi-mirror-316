import json
import socket
import time
from threading import Thread
from typing import Self

from tenacity import retry, wait_fixed

import nacos
from nacos.exception import NacosRequestException
from src.common.logger import logger
from src.config import settings


def get_host_ip():
    return socket.gethostbyname(socket.gethostname())


def load_config(content):
    if content:
        _config = json.loads(content)
        return _config
    return None


def nacos_config_callback(args):
    content = args["raw_content"]
    return load_config(content)


class PyNacosClient:
    service_name = settings.NACOS_SERVICE_NAME
    service_port = settings.PORT
    service_group = settings.NACOS_GROUP_NAME

    def __init__(self, server_addresses, namespace):
        self.server_addresses = server_addresses
        self.namespace = namespace
        self.service_ip = get_host_ip()
        self._ns_client: nacos.NacosClient = None

    @property
    def ns_client(self) -> nacos.NacosClient:
        return self._ns_client

    @ns_client.getter
    def ns_client(self) -> nacos.NacosClient:
        if self._ns_client is None:
            self._ns_client = nacos.NacosClient(
                server_addresses=self.server_addresses, namespace=self.namespace
            )

        return self._ns_client

    @retry(wait=wait_fixed(5))
    def register(self) -> Self:
        try:
            self.ns_client.add_naming_instance(
                self.service_name,
                self.service_ip,
                self.service_port,
                group_name=self.service_group,
            )
        except NacosRequestException as e:
            logger.error(f"服务注册nacos失败, 正在重试...: {repr(e)}")
            raise NacosRequestException(e)

        return self

    def modify(self, service_name, service_ip=None, service_port=None) -> None:
        self.ns_client.modify_naming_instance(
            service_name,
            service_ip if service_ip else self.service_ip,
            service_port if service_port else self.service_port,
        )

    def unregister(self) -> None:
        try:
            self.ns_client.remove_naming_instance(
                self.service_name, self.service_ip, self.service_port
            )
        except NacosRequestException as e:
            logger.error(f"服务注销nacos失败: {repr(e)}")

    def send_heartbeat(self) -> None:
        def heartbeat():
            while True:
                try:
                    self.ns_client.send_heartbeat(
                        self.service_name, self.service_ip, self.service_port
                    )
                    logger.info("heartbeat to Nacos server success")
                    time.sleep(5)
                except Exception as e:
                    logger.error(f"服务向Nacos发送心跳失败: {repr(e)}")
                    self.register()

        beat_thread = Thread(target=heartbeat)
        beat_thread.start()

    def load_conf(self, data_id, group) -> str:
        return self.ns_client.get_config(data_id=data_id, group=group, no_snapshot=True)

    def add_conf_watcher(self, data_id, group, callback) -> None:
        self.ns_client.add_config_watcher(data_id=data_id, group=group, cb=callback)


ns = PyNacosClient(settings.NACOS_SERVER_ADDRESSES, settings.NACOS_NAMESPACE)
