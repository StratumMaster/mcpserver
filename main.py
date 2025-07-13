from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount, Route

# 1. Create your FastAPI app with normal routes
app = FastAPI(title="My MCP FastAPI Server", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "FastMCP server is running"}

@app.get("/health")
async def health_check(request: Request):
    return JSONResponse({"status": "healthy"})

# 2. Create FastMCP from FastAPI (without transport param)
mcp = FastMCP.from_fastapi(app=app, path="/mcp")

# 3. Define MCP tools on mcp instance
@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def analyze(data: str) -> dict:
    return {"result": f"Analyzed: {data}"}

# 4. Create a Starlette app with the streaming (SSE) MCP http_app mounted separately
sse_app = mcp.http_app(transport="sse")  # explicit SSE streaming app

# Optional: add some test or health routes on sse_app
@sse_app.route("/test")
async def sse_test(request):
    return JSONResponse({"status": "SSE works"})

@sse_app.route("/")
async def sse_health(request):
    return JSONResponse({"status": "SSE HealthCheck works"})

# 5. Mount the FastAPI app and the SSE MCP app together using Starlette
starlette_app = Starlette(
    routes=[
        Mount("/", app=app),                # Your FastAPI app routes
        Mount("/mcp-server", app=mcp.http_app()),  # MCP API endpoint (non-streaming)
        Mount("/mcp-sse", app=sse_app),    # MCP SSE streaming endpoint
    ],
    lifespan=mcp.http_app().lifespan
)

# 6. Export starlette_app as the ASGI app for uvicorn
app = starlette_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
