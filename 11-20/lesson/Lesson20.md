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

# :books: 反应代理(ReAct Agent) - 流式输出执行过程

操作步骤

+ 继续上期内容，使用反应代理，流式输出代理执行过程
+ 编写样例程序

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
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()  # 读取.env文件

@tool
def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["tyo", "tokyo", "东京"]:
        return "25°C"
    else:
        return "28°C"

@tool
def get_coolest_cities():
    """Get a list of coolest cities"""
    return ["Tokyo", "New York", "Los Angeles"]

# 工具数组
tools = [get_weather, get_coolest_cities]
tool_node = ToolNode(tools=tools)
# LLM模型
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
# 创建一个与利用工具调用的聊天模型配合使用的图表代理
agent = create_react_agent(model, tools)
# agent.get_graph().draw_mermaid_png(output_file_path="graph.png")

# 最冷城市的天气是多少？
messages = {"messages": [("human", "what's the weather in the coolest cities?")]}

import asyncio

async def main():

    # 在调用每个节点后对图形状态的更新
    async for chunk in agent.astream(messages, stream_mode="updates"):
        for node, values in chunk.items():
            print("-" * 100)
            print(f"输出更新节点内容: '{node}'")
            print(values)
    print("=" * 100)
    print(chunk["agent"]["messages"][-1].content)

# 使用 asyncio.run 来运行 main 协程
asyncio.run(main())

print()
print("Done!")
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

