from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


from claude_chat.chain import chain as claude_chat_chain

add_routes(app, claude_chat_chain, path="/claude-chat")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
