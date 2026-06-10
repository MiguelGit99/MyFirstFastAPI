from fastapi import APIRouter, Cookie, Response

router = APIRouter(
    prefix='/cookies',
    tags=["Cookies"],               # Groups in docs
    responses={404: {"description": "Not found"}}
)


##########################
### Read & Set/Delete Cookies
##########################
# Read cookies
@router.get("/")
async def read_items(
    session_id: str | None = Cookie(default=None),
    tracking: str | None = Cookie(default=None),
):
    return {"session": session_id, "tracking": tracking}


@router.post("/login")
def set_cookies_login(response: Response):
    # Esto guarda las cookies en el navegador del cliente
    response.set_cookie(key="session_id", value="usuario_12345_abc")
    response.set_cookie(key="tracking", value="campana_marketing_2026")
    return {"message": "logged in"}

# Delete a cookie
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="session_id")
    return {"message": "logged out"}

