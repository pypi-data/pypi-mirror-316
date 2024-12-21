from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
import mcp.types as types
import mcp.server.stdio
from .wolfram_client import client

server = Server("MCP-wolfram-alpha")


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    """
    return [
        types.Prompt(
            name="wa",
            description="Ask Wolfram Alpha a question",
            arguments=[
                types.PromptArgument(
                    name="query",
                    description="query to ask Wolfram Alpha",
                    required=True,
                )
            ],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt by combining arguments with server state.
    """

    # TODO: Implement checks for this
    assert arguments is not None, "Arguments are required"

    return types.GetPromptResult(
        description="Ask Wolfram Alpha a question",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Use wolfram alpha to answer the following question: {arguments['query']}",
                ),
            )
        ],
    )


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="query-wolfram-alpha",
            description="Use Wolfram Alpha to answer a question. This tool should be used when you need complex math or symbolic intelligence.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"}  # Correct property: `query` with type `string`
                },
                "required": ["query"]  # Marking `query` as required
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    if not arguments:
        raise ValueError("Missing arguments")

    if name == "query-wolfram-alpha":
        try:
            response = await client.aquery(input=arguments["query"])
            result_text = next(response.results).text
        except Exception as e:
            result_text = "Error: Failed to query Wolfram Alpha: " + str(e)

        return [
            types.TextContent(
                type="text",
                text=result_text,
            )
        ]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="MCP-wolfram-alpha",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
