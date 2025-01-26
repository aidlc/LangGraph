import os, pprint, json, time
from langchain_openai import ChatOpenAI
from common import *
from dotenv import load_dotenv
from langgraph.graph.message import MessageGraph
from langgraph.graph import END, START

print("=" * 100)
start_time = time.time()  # 获取开始时间
load_dotenv()

####################################################################################################
## Nodes
def action1(state):
    print("\n--- Action1 ---")
    print(state)
    return [("assistant", "你好，我可以帮助你吗？😃")]

####################################################################################################
## Graph
graph = MessageGraph()
graph.add_node("action1", action1)

graph.add_edge(START, "action1")
graph.add_edge("action1", END)

app = graph.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")

# 详细指定属性
result = app.invoke([{"role": "user", "content": "Hello AI."}])

print("\n--- Final Result ---")
pprint.pprint(result)

print(evalEndTime(start_time))