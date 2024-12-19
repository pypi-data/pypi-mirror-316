import os
import yaml
from gai.lib.common.utils import get_app_path
from gai.lib.config.pydantic.gai_config import ClientConfig,ClientCategoryConfig,ClientLLMConfig

def get_gai_config(file_path=None):
    app_dir=get_app_path()
    global_lib_config_path = os.path.join(app_dir, 'gai.yml')
    if file_path:
        global_lib_config_path = file_path
    with open(global_lib_config_path, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    
def save_gai_config(config, file_path=None):
    app_dir=get_app_path()
    global_lib_config_path = os.path.join(app_dir, 'gai.yml')
    if file_path:
        global_lib_config_path = file_path
    with open(global_lib_config_path, 'w') as f:
        yaml.dump(config, f, sort_keys=False)
    
def get_gai_url(category_name):
    config = get_gai_config()
    key = f"gai-{category_name}"
    url = config["clients"][key]["url"]
    return url

# "api_url" property contains the fully qualified domain name of this API server
def get_api_url():
    config = get_gai_config()
    url = config["api_url"]
    return url

def get_client_config(config_type_or_name:str, file_path:str=None) -> ClientLLMConfig:
    config = get_gai_config(file_path=file_path)
    config = ClientConfig.from_config(config)
    
    # Dynamically access the category attribute
    name_parts = config_type_or_name.split("-")
    type_ = name_parts[0]
    category_config:ClientCategoryConfig = getattr(config, type_, None)
    
    if category_config is None:
        raise ValueError(f"Config type {type_} not found in config")
    
    if len(name_parts) == 1:
        # This means that the default llm config is requested
        default = category_config.default
        return category_config.configs[default]
    
    return category_config.configs[config_type_or_name]


