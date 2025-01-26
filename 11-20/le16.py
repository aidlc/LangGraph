import pprint
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain import globals

# 设置调试模式
globals.set_debug(False)

@tool
def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["tyo", "tokyo"]:
        return location + "->" + "下雨"
    else:
        return location + "->" + "晴天"

@tool
def get_coolest_cities():
    """Get a list of coolest cities"""
    return ["Tokyo", "New York", "Los Angeles"]

tools = [get_weather, get_coolest_cities]
tool_node = ToolNode(tools=tools)

###############################################################################
# 手动调用 ToolNode

# 调用单个工具(模拟AI调用，所以使用AIMessage)
message_with_tool_call = AIMessage(
    content="",
    tool_calls=[
        {
            "name": "get_weather",
            "args": {"location": "LA"},
            # "args": {"location": "Tokyo"},
            "id": "1",
            "type": "tool_call",
        }
    ],
)

# 调用多个工具
# message_with_tool_call = AIMessage(
#     content="",
#     tool_calls=[
#         {
#             "name": "get_weather",
#             "args": {"location": "Tokyo"},
#             "id": "1",
#             "type": "tool_call",
#         },
#         {
#             "name": "get_coolest_cities",
#             "args": {},
#             "id": "2",
#             "type": "tool_call",
#         },
#     ],
# )

# 调用 ToolNode
response = tool_node.invoke({"messages": [message_with_tool_call]})
pprint.pprint(response)