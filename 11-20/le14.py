import os, pprint, json, time
from langchain_openai import ChatOpenAI
from common import *
from dotenv import load_dotenv
from langgraph.graph.message import MessageGraph
from langchain_core.messages import ToolMessage
from langgraph.graph import END, START

print("=" * 100)
start_time = time.time()  # 获取开始时间
load_dotenv()

####################################################################################################
## Nodes
def action1(state):
    print("\n--- Action1 ---")
    print(state)
    return [("assistant", "你好，我需要调用工具帮你处理问题。😃")]

def tool1(state):
    print("\n--- Tool1 ---")
    print(state)
    # 将执行工具后的结果传递回模型的消息。工具消息包含工具调用的结果。通常，结果被编码放在 content 字段中。
    return [ToolMessage(tool_call_id="call_tool1_12345", content="2", artifact="回答用户提问:1+1=2")]

####################################################################################################
## Graph
graph = MessageGraph()
graph.add_node("action1", action1)
graph.add_node("tool1", tool1)

graph.add_edge(START, "action1")
graph.add_edge("action1", "tool1")
graph.add_edge("tool1", END)

app = graph.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")

# 详细指定属性
result = app.invoke([{"role": "user", "content": "Hello AI."}])

print("\n--- Final Result ---")
pprint.pprint(result)

print(evalEndTime(start_time))