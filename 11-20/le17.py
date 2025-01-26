from dotenv import load_dotenv
load_dotenv()  # 读取.env文件
import pprint
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain import globals
from langchain_openai import ChatOpenAI
globals.set_debug(False)

@tool
def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["tyo", "tokyo", "东京"]:
        return location + "->" + "下雨"
    else:
        return location + "->" + "晴天"

@tool
def get_coolest_cities():
    """Get a list of coolest cities"""
    return ["Tokyo", "New York", "Los Angeles"]

# 工具数组
tools = [get_weather, get_coolest_cities]
# 创建一个工具节点
tool_node = ToolNode(tools=tools)

# 创建一个带有工具的模型
model_with_tools = ChatOpenAI(model_name="gpt-4o-mini", temperature=0).bind_tools(tools)

# 调用模型执行用户请求
result = model_with_tools.invoke(input="请告诉我东京的天气？")
pprint.pprint(type(result))  # AIMessage

# 执行结果是返回工具调用请求(说明LLM无法处理用户的请求，需要调用工具)
pprint.pprint(result.tool_calls)
"""
[{'args': {'location': 'Tokyo'},
  'id': 'call_b7DWLNYHzI9wdCk6iNTOUfDZ',
  'name': 'get_weather',
  'type': 'tool_call'}]
"""

# 执行工具调用
result = tool_node.invoke({"messages": [result]})
pprint.pprint(result)
"""
{'messages': [ToolMessage(content='Tokyo->下雨', name='get_weather', tool_call_id='call_b7DWLNYHzI9wdCk6iNTOUfDZ')]}
"""