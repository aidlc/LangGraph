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

# :books: 反应代理(ReAct Agent) - 配置系统消息

操作步骤

+ 配置代理的系统消息 SystemMessage
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
import time
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain import globals
import common

# 输出详细的调试信息
# globals.set_debug(True)

start_time = time.time()  # 获取开始时间

@tool
def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["tyo", "tokyo", "东京"]:
        return "25°C"
    else:
        return "28°C"

# 工具数组
tools = [get_weather]
tool_node = ToolNode(tools=tools)
# LLM模型
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# 创建一个与利用工具调用的图表代理
system_prompt = "你是一名翻译专家，你的任务是将用户输入的英文文本翻译到中文。"
agent = create_react_agent(model=model, tools=tools, state_modifier=system_prompt)

# 用户提示词
messages = {"messages": [("human", "what's the weather in Tokyo?")]}
# messages = {"messages": [("human", "what's the weather in Osaka?")]}
# messages = {"messages": [("human", "book")]}
# messages = {"messages": [("human", "lesson")]}

def call_agent(messages):
    response = agent.invoke(messages)
    last_message = response["messages"][-1]
    return last_message.content

# 调用函数并打印结果
print(call_agent(messages))

print()
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

