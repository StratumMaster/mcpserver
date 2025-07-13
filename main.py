from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastmcp import FastMCP

# Create FastAPI app
app = FastAPI(title="My MCP FastAPI Server", version="1.0.0")

# Root route
@app.get("/")
async def root():
    return {"message": "FastMCP server is running"}

# Custom health check route
@app.get("/health")
async def health_check(request: Request):
    return JSONResponse({"status": "healthy"})

# Create MCP instance from FastAPI app
mcp = FastMCP.from_fastapi(app=app, transport="sse", path="/mcp")

# Define MCP tools directly on mcp instance

@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def analyze(data: str) -> dict:
    return {"result": f"Analyzed: {data}"}

if __name__ == "__main__":
    mcp.run()  # Runs standalone server (like uvicorn)
