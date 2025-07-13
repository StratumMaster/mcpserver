from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

# Create your FastMCP server
mcp = FastMCP("MyServer")

# Create the ASGI app for MCP
mcp_app = mcp.http_app(path='/mcp')

# For legacy SSE transport (deprecated)
sse_app = mcp.http_app(transport="sse")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    return JSONResponse({"status": "healthy"})

# Define a root route handler
async def root(request):
    return JSONResponse({"message": "FastMCP server is running"})

@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def analyze(data: str) -> dict:
    return {"result": f"Analyzed: {data}"}

# Create a Starlette app with root route and MCP mount
app = Starlette(
    routes=[
        Route("/", endpoint=root),
        Mount("/mcp-server", app=mcp_app),
    ],
    lifespan=mcp_app.lifespan,
)
