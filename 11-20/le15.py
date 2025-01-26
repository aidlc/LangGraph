import random
from operator import add
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

    state: Annotated[List, add]


################################################################################
# SubGraphA

actionA1_name = "(actionA1)"
actionA2_name = "(actionA2)"
subGraphA_name = "(subGraphA)"

# Nodes


def actionA1(state):
    print(">", actionA1_name, state)
    return {"state": [f"{actionA1_name} ok"]}


def actionA2(state):
    print(">", actionA2_name, state)
    return {"state": [f"{actionA2_name} ok"]}


# Graph

subgraphA = StateGraph(GraphState)
subgraphA.add_node(actionA1_name, actionA1)
subgraphA.add_node(actionA2_name, actionA2)
subgraphA.add_edge(START, actionA1_name)
subgraphA.add_edge(actionA1_name, actionA2_name)
subgraphA.add_edge(actionA2_name, END)
graphA = subgraphA.compile()
graphA.get_graph().draw_mermaid_png(output_file_path="subGraphA.png")


################################################################################
# SubGraphB

actionB1_name = "(actionB1)"
actionB2_name = "(actionB2)"
subGraphB_name = "(subGraphB)"

# Nodes
def actionB1(state):
    print(">", actionB1_name, state)
    return {"state": [f"{actionB1_name} ok"]}


def actionB2(state):
    print(">", actionB2_name, state)
    return {"state": [f"{actionB2_name} ok"]}


# Graph

subgraphB = StateGraph(GraphState)
subgraphB.add_node(actionB1_name, actionB1)
subgraphB.add_node(actionB2_name, actionB2)
subgraphB.add_edge(START, actionB1_name)
subgraphB.add_edge(actionB1_name, actionB2_name)
subgraphB.add_edge(actionB2_name, END)
graphB = subgraphB.compile()
graphB.get_graph().draw_mermaid_png(output_file_path="subGraphB.png")

################################################################################
# MainGraph

action1_name = "(action1)"
action2_name = "(action2)"


# Nodes


def action1(state):
    print(">", action1_name, state)
    return {"state": [f"{action1_name} ok"]}


def action2(state):
    print(">", action2_name, state)
    return {"state": [f"{action2_name} ok"]}


graph = StateGraph(GraphState)

graph.add_node(action1_name, action1)
graph.add_node(action2_name, action2)
graph.add_node(subGraphA_name, graphA)
graph.add_node(subGraphB_name, graphB)
graph.add_edge(START, action1_name)
graph.add_edge(action1_name, subGraphA_name)
graph.add_edge(action1_name, subGraphB_name)
graph.add_edge([subGraphA_name, subGraphB_name], action2_name)
graph.add_edge(action2_name, END)

app = graph.compile()
app.get_graph(xray=False).draw_mermaid_png(output_file_path="graph.png")

# 只返回结果
result = app.invoke({"state": ["initial"]})
print("---Final Result---\n", result)

print(evalEndTime(start_time))