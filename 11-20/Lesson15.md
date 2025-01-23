---
marp: true
theme: default
header: 'LangGraph 开发课程'
footer: '小马技术 - https://youtube.com/@deeplearncloud'
style: |
  header {
    color: #00ced1;
    font-weight: bold;
    font-size: 18px !important;
  }
  footer {
    color: #50fa7b;
    font-weight: bold;
    font-size: 18px !important;
  }
  footer a {
    font-size: 18px !important;
    color: #009dd5;
  }
  h1 {
    color: #f8f8f2;
    font-size: 64px;
  }
  section {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    background-color: #154360;
    color: #f8f8f2;
    font-size: 24px;
    font-family: Yuanti SC;
  }
  a {
    color: #8be9fd;
  }
  img {
    background-color: transparent!important;
  }
  code {
    font-family: JetBrains Mono;
  }

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 120px;
    margin: 0;
  }
  h2 {
    margin: 0;
    font-size: 42px;
  }
</style>

![width:300px drop-shadow:0,5px,10px,rgba(f,f,f,.4)](./images/langchain.png)

# LangGraph

## 构建复杂的 AI 应用程序

---
<style scoped>
  section {
    font-size: 40px;
  }
  h1 {
    font-size: 50px;
    color: #f8f8f2;
  }
  li {
    font-family: JetBrains Mono;
    font-size: 32px;
  }
</style>

# :books: SubGraph - 实现子图

操作步骤

+ 对于可重复使用的流程，可以将其封装为子图
+ 编写样例程序

---
<style scoped>
  h1 {
    font-size: 64px;
    color: #f8f8f2;
    margin: 0;
  }
  section {
    align-items: center;
    justify-content: center;
  }
  img {
    border-radius: 2%;
    margin: 0;
    border: 10px solid #f8f8f2;
    box-shadow: 2px 2px 3px black;
    background-color: white !important;
    padding: 5px;
  }
</style>

# 系统架构

![width:230px](./images/Lesson15a.png)

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 200px;
    margin: 0;
  }
  img {
    border: 10px solid #f8f8f2;
    border-radius: 20%;
    margin: 0;
    box-shadow: 2px 2px 3px black;
  }
</style>

![width:200px](../images/step-by-step-operation.webp)

# 操作演示

---
<style scoped>
  h3 {
    margin-top: 0;
  }
  pre {
    box-shadow: 2px 2px 3px black;
  }
</style>
### main.py

```python
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
```

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 200px;
  }
</style>

# 下课时间

