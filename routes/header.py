from fastapi import APIRouter, Header

router = APIRouter(
    prefix='/header',
    tags=["Items"],               # Groups in docs
    responses={404: {"description": "Not found"}}
)

##########################
### Read Header data
##########################
@router.get("/items1")
async def read_items(
    user_agent: str | None = Header(default=None),
    x_request_id: str | None = Header(default=None),
    accept_language: str | None = Header(default=None),
):
    return {"user_agent": user_agent, "request_id": x_request_id}
# Header("X-Request-Id") auto-converts to x_request_id (underscore)

# Duplicate headers (e.g., multiple X-Token values)
@router.get("/items2")
async def read_items(x_token: list[str] | None = Header(default=None)):
    return {"tokens": x_token}

