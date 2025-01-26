from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()  # 读取.env文件

@tool
def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["tyo", "tokyo", "东京"]:
        return "25°C"
    else:
        return "28°C"

@tool
def get_coolest_cities():
    """Get a list of coolest cities"""
    return ["Tokyo", "New York", "Los Angeles"]

# 工具数组
tools = [get_weather, get_coolest_cities]
tool_node = ToolNode(tools=tools)
# LLM模型
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
# 创建一个与利用工具调用的聊天模型配合使用的图表代理
agent = create_react_agent(model, tools)

# 最冷城市的天气是多少？
messages = {"messages": [("human", "what's the weather in the coolest cities?")]}

# 调用代理
result = agent.invoke(messages)
print(result["messages"][-1].content)

# 流式输出
# for chunk in agent.stream(
#     messages,
#     stream_mode="values",
# ):
#     chunk["messages"][-1].pretty_print()

print()
print("Done!")