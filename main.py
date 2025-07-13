from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

# 1. FastAPI app with your normal routes
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastMCP + FastAPI running"}

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "healthy"})

# 2. Create MCP with SSE enabled, using FastAPI OpenAPI spec
mcp_sse = FastMCP(
    openapi_spec=app.openapi(),
    path="/mcp",
    transport="sse",    # <-- streaming enabled here
)

# 3. Define MCP tools on mcp_sse instance if needed
@mcp_sse.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

@mcp_sse.tool
def analyze(data: str) -> dict:
    return {"result": f"Analyzed: {data}"}

# 4. Create Starlette app mounting your FastAPI routes AND MCP SSE app at /mcp
starlette_app = Starlette(
    routes=[
        Mount("/", app=app),                # your FastAPI app routes
        Mount("/mcp", app=mcp_sse.http_app()),  # MCP with SSE streaming at /mcp
    ],
    lifespan=mcp_sse.http_app().lifespan,
)

# 5. Export starlette_app as app for uvicorn
app = starlette_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
