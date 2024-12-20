from nonebot.plugin import get_plugin_config
from pydantic import BaseModel

class Config(BaseModel):
    uin: str = ""
    skey: str = ""

config = get_plugin_config(Config)
