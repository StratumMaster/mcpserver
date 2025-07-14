import asyncio
import httpx
from jsonschema import validate, ValidationError

async def register_tools_from_remote_json_async(tool_definitions_url: str, mcp):
    # Fetch JSON tool definitions asynchronously
    async with httpx.AsyncClient() as client:
        response = await client.get(tool_definitions_url)
        response.raise_for_status()
        tool_definitions = response.json()

    for tool in tool_definitions:
        name = tool["name"]
        description = tool.get("description", "")
        tags = set(tool.get("tags", []))
        endpoint = tool["endpoint"]
        input_schema = tool.get("input_schema", {})
        output_schema = tool.get("output_schema", {})

        # Build function signature string with explicit params
        params_code = []
        for param, typ in input_schema.items():
            if typ.endswith("?"):
                params_code.append(f"{param}=None")  # Optional param default None
            else:
                params_code.append(param)
        params_str = ", ".join(params_code)

        # Build async function code as string
        fn_code = f"""
import httpx
from jsonschema import validate, ValidationError

async def tool_fn({params_str}):
    payload = {{}}
"""
        # Add parameter-to-payload logic
        for param, typ in input_schema.items():
            if typ.endswith("?"):
                fn_code += f"    if {param} is not None:\n        payload['{param}'] = {param}\n"
            else:
                fn_code += f"    payload['{param}'] = {param}\n"

        fn_code += f"""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post("{endpoint}", json=payload)
            resp.raise_for_status()
            result = resp.json()
        except Exception as e:
            return {{'error': str(e)}}

    schema = {output_schema}
    try:
        validate(instance=result, schema=schema)
    except ValidationError as e:
        return {{'error': 'Output schema validation failed', 'details': str(e)}}

    return result
"""

        # Prepare exec environment and exec the function code
        exec_env = {}
        exec(fn_code, exec_env)
        fn = exec_env['tool_fn']

        # Register the async function with mcp.tool
        mcp.tool(name=name, description=description, tags=tags)(fn)
