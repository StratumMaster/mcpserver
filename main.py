from fastapi import FastAPI
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

# Step 1: Define your FastAPI app with normal routes
fastapi_app = FastAPI(title="My API", version="1.0.0")

@fastapi_app.get("/items", tags=["items"], operation_id="list_items")
def list_items():
    return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]

@fastapi_app.get("/items/{item_id}", tags=["items"], operation_id="get_item")
def get_item(item_id: int):
    return {"id": item_id, "name": f"Item {item_id}"}

@fastapi_app.post("/items", tags=["items"], operation_id="create_item")
def create_item(name: str):
    return {"id": 3, "name": name}

# Step 2: Create FastMCP from FastAPI app
mcp = FastMCP.from_fastapi(app=fastapi_app)

# Step 3: Create MCP ASGI apps (REST and SSE)
mcp_http_app = mcp.http_app()
mcp_sse_app = mcp.http_app(transport="sse")

# Step 4: Combine them with Starlette
app = Starlette(
    routes=[
        Mount("/", app=fastapi_app),        # Your native FastAPI app
        Mount("/mcp", app=mcp_http_app),    # REST/stream-compatible MCP
        Mount("/mcp-sse", app=mcp_sse_app), # Explicit SSE transport
    ],
    lifespan=mcp_http_app.lifespan,
)
