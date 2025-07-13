import httpx
from jsonschema import validate, ValidationError

def parse_value(value, type_str):
    if type_str.endswith("?"):
        if value is None:
            return None
        base_type = type_str[:-1]
    else:
        base_type = type_str

    type_map = {
        "string": str,
        "int": int,
        "integer": int,
        "bool": lambda v: str(v).lower() in ["true", "1", "yes"],
        "float": float
    }
    parser = type_map.get(base_type)
    if parser is None:
        raise ValueError(f"Unsupported type '{base_type}'")
    return parser(value)

async def register_tools_from_remote_json_async(tool_definitions_url: str, mcp):
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

        def make_tool_fn(endpoint_url, input_schema_dict, output_schema_dict):
            async def tool_fn(**kwargs) -> dict:
                input_payload = {}
                for param, param_type in input_schema_dict.items():
                    val = kwargs.get(param)
                    if val is None and param_type.endswith("?"):
                        input_payload[param] = None
                        continue
                    if val is None:
                        return {"error": f"Missing required parameter: {param}"}
                    try:
                        input_payload[param] = parse_value(val, para
