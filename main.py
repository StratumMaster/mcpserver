from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route
from starlette.requests import Request

# Create your FastMCP server with both OpenAPI and SSE support
mcp = FastMCP("MyServer")
mcp_app = mcp.http_app(path='/mcp', transport="sse")

# Custom health check endpoint
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    return JSONResponse({"status": "healthy"})

# Define root Starlette route (optional)
async def root(request):
    return JSONResponse({"message": "FastMCP server is running"})

# Register FastMCP tools
@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def analyze(data: str) -> dict:
    return {"result": f"Analyzed: {data}"}

# Build final Starlette app
app = Starlette(
    routes=[
        Route("/", endpoint=root),
