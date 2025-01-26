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

# :books: 反思代理设计 - 我的代理会反思

操作步骤

+ 使用流图实现自我反思设计
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

![width:680px](./images/Lesson23a.png)

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

