from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route
from starlette.requests import Request
from starlette.responses import RedirectResponse
from dynamic_tools import register_tools_from_remote_json_async

# Create your FastMCP server
mcp = FastMCP("MyServer")

# Create the ASGI app for MCP with SSE transport
mcp_app = mcp.http_app(path='/mcp', transport="sse")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    return JSONResponse({"status": "healthy"})

# Root route handler
async def root(request):
    return JSONResponse({"message": "FastMCP server is running"})

# Define Dynamic MCP tools
tool_schema_url = "https://my-json-server.typicode.com/StratumMaster/samplejson/config"
await register_tools_from_remote_json_async(tool_schema_url, mcp)

# Define MCP tools
@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def analyze(data: str) -> dict:
    return {"result": f"Analyzed: {data}"}

# Optional redirect to ensure trailing slash on SSE base URL
@mcp_app.route("/mcp-sse")
async def redirect_sse(request):
    return RedirectResponse(url="/mcp-sse/")

@mcp_app.route("/")
async def sse_health(request):
    return JSONResponse({"status": "SSE HealthCheck works"})

# Create Starlette app with root and MCP mount
app = Starlette(
    routes=[
        Route("/", endpoint=root),
        Mount("/mcp-server", app=mcp_app),  # <-- MCP server mounted here
    ],
    lifespan=mcp_app.lifespan,
)
