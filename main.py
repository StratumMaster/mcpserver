from fastapi import FastAPI
from fastmcp import FastMCP

app = FastAPI(title="My MCP Server", version="1.0.0")
mcp = FastMCP.from_fastapi(app=app)

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
