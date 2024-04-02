#pylint: disable=missing-function-docstring,wrong-import-position

import os
import secrets

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# The following section is adapted from
# https://github.com/tiangolo/fastapi/issues/364
# We are disabling the default docs and
# recreating them behind some basic authentication
app = FastAPI(
    title="Claude Chat",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url = None,
)

router = APIRouter()

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, os.getenv('BEDROCK_CHAT_USERNAME', 'bedrock'))
    correct_password = secrets.compare_digest(
        credentials.password, os.getenv('BEDROCK_CHAT_PASSWORD', 'bedrock'))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/health", include_in_schema=False)
async def health():
    content = """
    <h3>Bedrock Chat is up and running!</h3>
    """
    return Response(content=content, status_code=200, media_type="text/html")

@router.get("/", include_in_schema=False)
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

@router.get("/docs", include_in_schema=False)
async def get_swagger_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@router.get("/redoc", include_in_schema=False)
async def get_redoc_documentation():
    return get_redoc_html(openapi_url="/openapi.json", title="docs")

@router.get("/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

###############
# Claude Chat #
###############

from langserve import add_routes

from claude_chat.chain import chain as claude_chat_chain

add_routes(router, claude_chat_chain, path="/claude-chat")

app.include_router(router, dependencies=[Depends(get_current_username)])

########
# Main #
########

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
