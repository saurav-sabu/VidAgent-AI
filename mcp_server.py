from mcp.server.fastmcp import FastMCP
from app import get_realtime_info, generate_video_script

mcp = FastMCP("VidAgent")


@mcp.tool()
async def get_latest_info_mcp(query):
    return get_realtime_info(query)


@mcp.tool()
async def generate_video_script_mcp(query):
    real_info = get_realtime_info(query)
    return generate_video_script(real_info)

if __name__ == "__main__":
    mcp.run(transport="stdio")



