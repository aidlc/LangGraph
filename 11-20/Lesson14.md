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

# :books: MessageGraph - 增加工具处理节点

操作步骤

+ 使用消息图，增加工具处理节点
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

![width:170px](./images/Lesson14a.png)

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

