"""endpoint about use cache."""

import pickle

from src.exceptions.core import APIException
from src.exceptions.error_messages import ErrorMessage
from fastapi import APIRouter, Depends
from starlette import status

from src.api.dependencies.redis import cache
from src.api.dependencies.supabase import supabase
from src.schemas.movie import MovieResponse
from src.schemas.dummy import DummyResponse

# from src.core.logger.logging_context_route import LoggingContextRoute
from loguru import logger
import traceback

router = APIRouter()
# router.route_class = LoggingContextRoute


@router.get("/", response_model=list[MovieResponse])
async def index(
    redis_client: cache = Depends(cache), supabase_client: supabase = Depends(supabase)
) -> list[MovieResponse]:
    """Endpoint about use Cache."""

    try:
        if (cached_data := redis_client.get("movies-python")) is not None:
            logger.info("Use Cache")
            return pickle.loads(cached_data)
        logger.info("Get Data From DB")
        response = supabase_client.table("movies").select("*").execute()
        movies = response.data
        redis_client.set("movies-python", pickle.dumps(movies))
        redis_client.expire("movies-python", 30)
        return movies
    except Exception as e:
        traceback.print_exc()
        raise APIException(ErrorMessage.FAILED_FETCH_DATA_FROM_MOVIE_TABLE)

@router.get(
    "/dummy",
    summary="Test Path After UpdatingDocker Image",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=DummyResponse,
)
def dummy() -> DummyResponse:
    """
    Call this path.

    If you push new Docker Image to ECR use "deploy.sh"
    """
    logger.info("Dummy")
    return DummyResponse(status="dummy")
