from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..services.methodology_service import (
    extract_methodologies,
    fetch_methodology_slugs,
)
from ..services.publication_service import fetch_publication_slugs
from ..services.release_service import extract_releases
from ..services.vector_db_client import recreate_collection, upsert_data

router = APIRouter(prefix="/api/maintenance")


@router.post(path="/publications/build")
async def build_publications() -> JSONResponse:
    try:
        upsert_data(records=extract_releases(slugs=fetch_publication_slugs()))
    except Exception as e:
        return JSONResponse(status_code=500, content={"Content": e})
    return JSONResponse(status_code=200, content={"Content": "Successful"})


@router.post(path="/methodologies/build")
async def build_methodologies() -> JSONResponse:
    try:
        upsert_data(records=extract_methodologies(slugs=fetch_methodology_slugs()))
    except Exception as e:
        return JSONResponse(status_code=500, content={"Content": e})
    return JSONResponse(status_code=200, content={"Content": "Successful"})


@router.delete(path="/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear() -> None:
    recreate_collection()
