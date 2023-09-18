from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..services.methodology_service import (
    extract_methodologies,
    fetch_methodology_slugs,
)
from ..services.publication_service import fetch_publication_slugs
from ..services.release_service import extract_releases
from ..services.vector_db_client import data_upsertion, recreate_collection

router = APIRouter(prefix="/api/maintenance")


@router.post("/publications/build")
async def build_publications():
    slugs = fetch_publication_slugs()
    try:
        data_upsertion(slugs, extract_releases)
    except Exception as e:
        return JSONResponse(status_code=500, content={"Content": e})
    return JSONResponse(status_code=200, content={"Content": "Successful"})


@router.post("/methodologies/build")
async def build_methodologies():
    slugs = fetch_methodology_slugs()
    try:
        data_upsertion(slugs, extract_methodologies)
    except Exception as e:
        return JSONResponse(status_code=500, content={"Content": e})
    return JSONResponse(status_code=200, content={"Content": "Successful"})


@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear():
    recreate_collection()
