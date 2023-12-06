from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..services.publication_service import delete_publication
from ..services.release_service import extract_releases
from ..services.vector_db_client import data_upsertion

router = APIRouter(prefix="/api/publications")


@router.post(path="/{slug}/update")
async def update(slug: str) -> JSONResponse:
    try:
        delete_publication(slug=slug)
        data_upsertion(records=extract_releases(slugs=[slug]))
    except Exception as e:
        return JSONResponse(status_code=500, content={"Content": e})
    return JSONResponse(status_code=200, content={"Content": "Successful"})
