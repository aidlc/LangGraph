import os, pprint, json, time
from typing import TypedDict
from langgraph.graph import StateGraph
from common import *
from dotenv import load_dotenv

print("=" * 100)
start_time = time.time()  # 获取开始时间
load_dotenv()

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    """
    state: str

graph = StateGraph(GraphState)
app = graph.compile()
result = app.invoke({"state": "helo langsmith!"})
print("result", result)

print(evalEndTime(start_time))