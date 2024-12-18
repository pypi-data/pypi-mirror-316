import os
from gai.lib.config.config_utils import get_gai_config
def test_get_gai_config():
    here = os.path.dirname(__file__)
    config_path =  os.path.abspath(os.path.join(here,"..","..","..","..","..","gai-data","src","gai","data","gai.yml"))
    config = get_gai_config(config_path)
    assert config["clients"]["ttt"]["default"]=="ttt-llamacpp-dolphin"

def test_get_client_config():
    here = os.path.dirname(__file__)
    config_path =  os.path.abspath(os.path.join(here,"..","..","..","..","..","gai-data","src","gai","data","gai.yml"))
    config = get_gai_config(config_path)
    
    from gai.lib.config.gai_config import ClientConfig
    client_config = ClientConfig.from_config(config)
    default = client_config.ttt.default
    assert client_config.ttt.default=="ttt-llamacpp-dolphin"
    assert client_config.ttt.configs[default].url=="http://localhost:12031/gen/v1/chat/completions"


