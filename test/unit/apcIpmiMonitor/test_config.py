import os

from apcIpmiMonitor.Config import Config
from apcIpmiMonitor.Domain.Server import Server

#todo: group tests that share configs

def test_config_parses_yaml_to_dict(root_path):
    config_rel_path = os.path.join("test", "fixtures", "apcIpmiMonitor", "Config", "simple_config.yaml")
    config = Config(os.path.join(root_path, config_rel_path))

    assert config.to_dict() == {
        "simple": {
            "key": "value",
            "array": ["value 1", "value 2"]
        }
    }

def test_config_loads_server_objects(root_path):
    config_rel_path = os.path.join("test", "fixtures", "apcIpmiMonitor", "Config", "simple_config.yaml")
    config = Config(os.path.join(root_path, config_rel_path))

    servers = config.get_servers()

    for server in servers:
        assert isinstance(Server, server)