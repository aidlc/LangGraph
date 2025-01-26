import pprint, time, random, operator
from typing import List, TypedDict, Optional, Annotated, Dict, Literal
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END, MessageGraph
import common
import step1, step2, step3

print("=" * 100)
start_time = time.time()  # 获取开始时间

####################################################################################################
## Names
# 构建名称：这里我们将构建共同的名称
draft_name = "(draft)"
revise_name = "(revise)"

tool_name = "(tool_node)"

####################################################################################################
## Nodes
# 构建节点：这里我们将构建所有的节点
def draft(state):
    print("---", draft_name, "---")
    response = step2.initial_answer_chain.invoke(state)
    return response

def revise(state):
    print("---", revise_name, "---")
    response = step3.revision_chain.invoke(state)
    return response

####################################################################################################
## Graph
# 构建图：这里我们将构建我们的图
graph = MessageGraph()

graph.add_node(draft_name, draft)
graph.add_node(tool_name, step1.tool_node)
graph.add_node(revise_name, revise)

graph.add_edge(START, draft_name)
graph.add_edge(draft_name, tool_name)
graph.add_edge(tool_name, revise_name)
graph.add_edge(revise_name, END)

app = graph.compile()
app.get_graph(xray=False).draw_mermaid_png(output_file_path="graph.png")

messages = [
    HumanMessage(content="三国演义的桃园结义都是谁?"),
]

result = app.invoke(messages)
print("-" * 100)
for msg in result:
    msg.pretty_print()

print(common.evalEndTime(start_time))