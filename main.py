from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")
app = mcp.app  # 👈 Add this line

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"
