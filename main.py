from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

# Create your FastMCP server
mcp = FastMCP("MyServer")

# Create the ASGI app
mcp_app = mcp.http_app(path='/mcp')

# Create a Starlette app and mount the MCP server
app = Starlette(
    routes=[
        Mount("/mcp-server", app=mcp_app),
        # Add other routes as needed
    ],
    lifespan=mcp_app.lifespan,
)
