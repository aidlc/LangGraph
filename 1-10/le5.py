import random
from typing import List, TypedDict, Optional, Annotated, Dict, Literal
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
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

action1_name = "(action1)"
action2_name = "(action2)"
action3_name = "(action3)"

def action1(state):
    print(">", action1_name, state)
    return {"state": f"{action1_name} ok"}

def action2(state):
    print(">", action2_name, state)
    return {"state": f"{action2_name} ok"}

def action3(state):
    print(">", action3_name, state)
    return {"state": f"{action3_name} ok"}

def condition_function(state) -> Literal["0", "1"]:
    return str(random.choice([0, 1]))

graph = StateGraph(GraphState)

graph.add_node(action1_name, action1)
graph.add_node(action2_name, action2)
graph.add_node(action3_name, action3)

graph.add_edge(START, action1_name)
graph.add_conditional_edges(
    action1_name, condition_function, {"0": action2_name, "1": action3_name}
)
graph.add_edge(action2_name, END)
graph.add_edge(action3_name, END)

app = graph.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")

# 只返回结果
result = app.invoke({"state": "initial"})
print(result)

# 流式返回
# for output in app.stream({"state": "initial"}):
#     for key, value in output.items():
#         # Node
#         print(f"Node '{key}':", value)

print(evalEndTime(start_time))