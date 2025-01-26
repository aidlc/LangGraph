import pprint, time, random, operator
from typing import List, TypedDict, Optional, Annotated, Dict, Literal
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END, MessageGraph
import common

print("=" * 100)
start_time = time.time()  # 获取开始时间

####################################################################################################
## Names
# 构建名称：这里我们将构建共同的名称
generation_name = "(generation)"
reflection_name = "(reflection)"

####################################################################################################
## States
# 构建状态：这里我们将构建流图的状态


####################################################################################################
## Nodes
# 构建节点：这里我们将构建所有的节点
def generation(state):
    print("---", generation_name, "---")
    pprint.pprint(state)
    return [AIMessage(f"{generation_name} ok")]

def reflection(state):
    print("---", reflection_name, "---")
    pprint.pprint(state)
    # 反思节点返回的是一个人类消息，模拟人类对AI生成的内容进行指摘
    return [HumanMessage(f"{reflection_name} ok")]

####################################################################################################
## Edges
# 构建边：这里我们将构建流图的边
def condition_function(state):
    print("---", "condition_function", "---")
    if len(state) < 5:
        return reflection_name
    else:
        return END

####################################################################################################
## Graph
# 构建图：这里我们将构建我们的图
graph = MessageGraph()

graph.add_node(generation_name, generation)
graph.add_node(reflection_name, reflection)

graph.add_edge(START, generation_name)
graph.add_conditional_edges(
    generation_name,
    condition_function,
)
graph.add_edge(reflection_name, generation_name)

app = graph.compile()
# app.get_graph(xray=False).draw_mermaid_png(output_file_path="graph.png")

messages = [
    SystemMessage("你是一位有用的AI助手。"),
    HumanMessage(f"你好"),
]

result = app.invoke(messages)
print("-" * 100)
pprint.pprint(result)

print(common.evalEndTime(start_time))
