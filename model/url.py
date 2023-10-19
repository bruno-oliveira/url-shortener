from datetime import datetime
from typing import Optional

import timestamp
from fastapi import FastAPI
from pydantic import BaseModel


class Url(BaseModel):
    url: str
    hash_key: str
    created_at: Optional[timestamp] = None


print(Url.model_validate({'hash_key': "aaa", 'url': "aaaa"}))
