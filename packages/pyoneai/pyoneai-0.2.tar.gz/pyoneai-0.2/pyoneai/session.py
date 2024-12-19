__all__ = ["Session"]

import os

from prometheus_api_client.prometheus_connect import PrometheusConnect

from .config import SessionConfig
from .drivers.xmlrpc import OnedServerProxy


# NOTE: This is just a temporary class and is going to be replaced.
# TODO: Implement this class.
class OneFlowClient:
    url: str
    session: str

    def __init__(self, url: str, session: str) -> None:
        self.url = url
        self.session = session


class Session:
    """
    Manage OpenNebula components session.

    Create and handle connection objects with the OpenNebula
    components: oned, OneFlow, and Prometheus.

    Parameters
    ----------
    config_path : str
        The path to the configuration file.

    Attributes
    ----------
    config : SessionConfig
        The configuration settings for the sessions.
    oned_client : OnedServerProxy
        OpenNebula driver to interact with OpenNebula XML-RPC API.
    oneflow_client : OneFlowClient
        OpenNebula driver to interact with OpenNebula OneFlow API.
    prometheus_client : PrometheusConnect
        Prometheus client to interact with OpenNebula Prometheus API.
    """

    config: SessionConfig
    oned_client: OnedServerProxy
    oneflow_client: OneFlowClient
    prometheus_client: PrometheusConnect

    def __init__(self, config_path: os.PathLike[str] | str = "") -> None:
        config = SessionConfig(config_path)
        self.config = config
        self.oned_client = OnedServerProxy(
            config.one_xmlrpc, config.oned_session
        )
        self.oneflow_client = OneFlowClient(
            config.oneflow_server, config.oneflow_session
        )
        self.prometheus_client = PrometheusConnect(config.prometheus_server)
