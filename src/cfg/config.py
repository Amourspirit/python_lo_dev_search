# coding: utf-8
import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AppConfig:
    
    lodoc_search: str
    """
    Search string usse for lodoc commands such as:
    
    https://duckduckgo.com/?q={0}+site:api.libreoffice.org/docs/idl/
    """


def read_config(config_file: str) -> AppConfig:
    """
    Gets config for given config file

    Args:
        config_file (str): Config file to load

    Returns:
        AppConfig: Configuration object
    """
    with open(config_file, 'r') as file:
        data = json.load(file)
        return AppConfig(**data)

def read_config_default() -> AppConfig:
    """
    Loads default configuration ``config.json``

    Returns:
        AppConfig: Configuration Object
    """
    root = Path(__file__).parent
    config_file = Path(root, 'config.json')
    return read_config(str(config_file))