from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route
from starlette.requests import Request

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

@sse_app.route("/test")
async def sse_test(request):
    return JSONResponse({"status": "SSE works"})

@sse_app.route("/mcp-sse")
async def redirect_sse(request):
    return RedirectResponse(url="/mcp-sse/")

@sse_app.route("/")
async def sse_health(request):
    return JSONResponse({"status": "SSE HealthCheck works"})

# Create a Starlette app with root route and MCP mount
app = Starlette(
    routes=[
        Route("/", endpoint=root),
        Mount("/mcp-server", app=mcp_app),
        Mount("/mcp-sse/", app=sse_app),  # <- SSE endpoint
    ],
    lifespan=mcp_app.lifespan,
)
