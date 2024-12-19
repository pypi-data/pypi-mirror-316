from datetime import datetime

from pydantic import BaseModel


class Credentails(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    login: str
    password: str
    access_until: datetime | None = None
    service_name: str
