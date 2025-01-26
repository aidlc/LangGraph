import time
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain import globals
import common

# 输出详细的调试信息
# globals.set_debug(True)

start_time = time.time()  # 获取开始时间

@tool
def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["tyo", "tokyo", "东京"]:
        return "25°C"
    else:
        return "28°C"

# 工具数组
tools = [get_weather]
tool_node = ToolNode(tools=tools)
# LLM模型
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# 创建一个与利用工具调用的图表代理
system_prompt = "你是一名翻译专家，你的任务是将用户输入的英文文本翻译到中文。"
agent = create_react_agent(model=model, tools=tools, state_modifier=system_prompt)

# 用户提示词
messages = {"messages": [("human", "what's the weather in Tokyo?")]}
# messages = {"messages": [("human", "what's the weather in Osaka?")]}
# messages = {"messages": [("human", "book")]}
# messages = {"messages": [("human", "lesson")]}

def call_agent(messages):
    response = agent.invoke(messages)
    last_message = response["messages"][-1]
    return last_message.content

# 调用函数并打印结果
print(call_agent(messages))

print()
print(common.evalEndTime(start_time))
