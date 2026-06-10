from enum import Enum
from fastapi import APIRouter, Path, Query

router = APIRouter(
    prefix='/parameters',
    tags=["Parameters"],               # Groups in docs
    responses={404: {"description": "Not found"}}
)

##########################
### Read Parameters in Path
##########################
# Basic path parameter — auto-converted to int
@router.get("/path/items/{item_id}", summary="Basic path parameter — auto-converted to int")
async def read_item(item_id: int):
    """ Basic path parameter — auto-converted to int """
    return {"item_id": item_id}
# GET /items/abc → 422 validation error (not an int)

# Path with validation constraints
@router.get("/path/users/{user_id}", summary="Path with validation constraints")
async def read_user(
    user_id: int = Path(
        gt=0,                  # Greater than 0
        le=1000,               # Less than or equal to 1000
        title="User ID",
        description="The ID of the user to retrieve",
    ),
):
    """ Path with validation constraints """
    return {"user_id": user_id}

# Enum path parameter — restricts to allowed values
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@router.get("/path/models/{model_name}", summary="Enum path parameter — restricts to allowed values")
async def get_model(model_name: ModelName):
    """ Enum path parameter — restricts to allowed values """
    return {"model": model_name.value}
# GET /models/invalid → 422 error

# Multiple path parameters
@router.get("/path/users/{user_id}/items/{item_id}", summary="Multiple path parameters")
async def read_user_item(user_id: int, item_id: int):
    """ Multiple path parameters """
    return {"user_id": user_id, "item_id": item_id}

# File path parameter
@router.get("/path/files/{file_path:path}", summary="File path parameter")
async def read_file(file_path: str):
    """ File path parameter """
    return {"file_path": file_path}
# GET /files/home/user/data.txt → file_path="home/user/data.txt"


##########################
### Read Parameters in Querystring
##########################
# Optional with defaults — any param not in the path is a query param
@router.get("/query/items1", summary="Optional with defaults")
async def read_items(skip: int = 0, limit: int = 10):
    """ Optional with defaults — any param not in the path is a query param """
    return {"skip": skip, "limit": limit}
# GET /items/?skip=5&limit=20

# Required query parameter (no default value)
@router.get("/query/search1", summary="Required query parameter")
async def search(q: str):
    """ Required query parameter (no default value) """
    return {"query": q}
# GET /search/ → 422 error (q is required)

# Optional query parameter
@router.get("/query/items2", summary="Optional query parameter")
async def read_items(q: str | None = None):
    """ Optional query parameter """
    return {"query": q}

# Query with validation
@router.get("/query/search2", summary="Query with validation")
async def search(
    q: str = Query(
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9 ]+$",
        title="Search query",
        description="The search term",
    ),
):
    """ Query with validation """
    return {"query": q}

# List query parameter
@router.get("/query/items3", summary="List query parameter")
async def read_items(tags: list[str] = Query(default=[])):
    """ List query parameter """
    return {"tags": tags}
# GET /items/?tags=foo&tags=bar → {"tags": ["foo", "bar"]}

# Deprecated parameter
@router.get("/query/items4", summary="Deprecated parameter")
async def read_items(
    q: str | None = Query(default=None, deprecated=True),
):
    """ Deprecated parameter """
    return {"query": q}

# Exclude from OpenAPI schema
@router.get("/query/items5", summary="Exclude from OpenAPI schema")
async def read_items(
    secret: str = Query(include_in_schema=False),
):
    """ Exclude from OpenAPI schema. Swagger not showing input param. """
    return {"secret": secret}

