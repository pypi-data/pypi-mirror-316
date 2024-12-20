import json
import os
from typing import Dict, Optional


class ApplicationConfig(Dict):
    instance = None

    def __init__(self, *args, **kwargs):
        # from env var or {}
        json_config = os.environ.get("APPLICATION_CONFIG", "{}")
        config = json.loads(json_config)
        super().__init__(config)

    @classmethod
    def resolve(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance


def get_config_value(key: str) -> Optional[str]:
    return ApplicationConfig.resolve().get(key, None)
