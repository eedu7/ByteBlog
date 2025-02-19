from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
    expires_in: int = Field(..., description="Expires in")
    token_type: int = Field("bearer", description="Token type")
