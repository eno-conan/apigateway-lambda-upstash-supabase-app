from pydantic import BaseModel


class MovieResponse(BaseModel):

    """Response model to validate and return when performing a health check."""

    id: int  # noqa: A003
    name: str
    description: str

    class Config:
        from_attributes = True
