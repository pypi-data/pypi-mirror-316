import pydantic
from pydantic import BaseModel

# 判断当前 Pydantic 版本
IS_PYDANTIC_V2 = pydantic.VERSION[0] == 2

class Config(BaseModel):
    uin: str = ""
    skey: str = ""

    if IS_PYDANTIC_V2:
        # Pydantic v2 使用 @field_validator
        from pydantic import field_validator

        @field_validator("uin", "skey", mode='before')
        @classmethod
        def str_fields(cls, v):
            return str(v)  # 强制转换为字符串
    else:
        # Pydantic v1 使用 @validator
        from pydantic import validator

        @validator("uin", "skey", pre=True)
        @classmethod
        def str_fields(cls, v):
            return str(v)  # 强制转换为字符串
