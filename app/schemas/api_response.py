from typing import Optional

from pydantic import BaseModel


class Apiresponse(BaseModel):

    status: str

    message: str

    data: Optional[dict] = None

    model_config = {
        "from_attributes": True
    }
    