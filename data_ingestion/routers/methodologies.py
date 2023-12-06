from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..services.methodology_service import delete_methodology, extract_methodologies
from ..services.vector_db_client import data_upsertion

router = APIRouter(prefix="/api/methodologies")


@router.post(path="/{slug}/update")
def update(slug: str) -> JSONResponse:
    try:
        delete_methodology(slug=slug)
        data_upsertion(records=extract_methodologies(slugs=[slug]))
    except Exception as e:
        return JSONResponse(status_code=500, content={"Content": e})
    return JSONResponse(status_code=200, content={"Content": "Succesful"})
