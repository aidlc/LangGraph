from typing import Literal
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
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

tools = [get_weather, get_coolest_cities]
tool_node = ToolNode(tools=tools)

model_with_tools = ChatOpenAI(model_name="gpt-4o-mini", temperature=0).bind_tools(tools)

def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

def agent(state: MessagesState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

# 建立工作流
workflow = StateGraph(MessagesState)

# Define the two nodes we will cycle between
workflow.add_node("agent", agent)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
)
workflow.add_edge("tools", "agent")

app = workflow.compile()
# app.get_graph().draw_mermaid_png(output_file_path="graph.png")

# 单工具调用
for chunk in app.stream(
    {"messages": [("human", "what's the weather in Tokyo?")]}, stream_mode="values"
):
    chunk["messages"][-1].pretty_print()

# 多工具联合调用
# for chunk in app.stream(
#     {
#         "messages": [("human", "what's the weather in the coolest cities?")]
#     },  # 最冷城市的天气是多少？
#     stream_mode="values",
# ):
#     chunk["messages"][-1].pretty_print()

# print(chunk)
print()
print("Done!")