from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

# Create your FastMCP server
mcp = FastMCP("MyServer")

# Create the ASGI app for MCP
mcp_app = mcp.http_app(path='/mcp')

# Define a root route handler
async def root(request):
    return JSONResponse({"message": "FastMCP server is running"})

# Create a Starlette app with root route and MCP mount
app = Starlette(
    routes=[
        Route("/", endpoint=root),
        Mount("/mcp-server", app=mcp_app),
    ],
    lifespan=mcp_app.lifespan,
)
