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

# :books: 为处理加上后续处理

操作步骤

+ 为处理2加上后续处理
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
  }
</style>

# 系统架构

![width:160px](./images/Lesson08a.png)

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

action1_name = "(action1)"
action2_name = "(action2)"
action2b_name = "(action2b)"
action3_name = "(action3)"
action4_name = "(action4)"

def action1(state):
    print(">", action1_name, state)
    return {"state": [f"{action1_name} ok"]}

def action2(state):
    print(">", action2_name, state)
    return {"state": [f"{action2_name} ok"]}

def action2b(state):
    print(">", action2b_name, state)
    return {"state": [f"{action2b_name} ok"]}

def action3(state):
    print(">", action3_name, state)
    return {"state": [f"{action3_name} ok"]}

def action4(state):
    print(">", action4_name, state)
    return {"state": [f"{action4_name} ok"]}

graph = StateGraph(GraphState)

graph.add_node(action1_name, action1)
graph.add_node(action2_name, action2)
graph.add_node(action2b_name, action2b)
graph.add_node(action3_name, action3)
graph.add_node(action4_name, action4)

graph.add_edge(START, action1_name)
graph.add_edge(action1_name, action2_name)
graph.add_edge(action1_name, action3_name)
graph.add_edge(action2_name, action2b_name)
graph.add_edge([action2b_name, action3_name], action4_name)
graph.add_edge(action4_name, END)

app = graph.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")

# 只返回结果
result = app.invoke({"state": ["initial"]})
print(result)

# 流式返回(描述具体的处理过程)
# for output in app.stream({"state": ["initial"]}):
#     for key, value in output.items():
#         # Node
#         print(f"Node '{key}':", value)

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

