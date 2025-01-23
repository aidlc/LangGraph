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

# :books: 工具调用 - 大语言模型调用工具

操作步骤

+ 通过提示词让大语言模型调用工具
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
    padding: 20px;
    border: 10px solid #f8f8f2;
    box-shadow: 2px 2px 3px black;
    background-color: white !important;
  }
</style>

# 系统架构

![width:500px](./images/Lesson17a.svg)

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
from dotenv import load_dotenv
load_dotenv()  # 读取.env文件
import pprint
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain import globals
from langchain_openai import ChatOpenAI
globals.set_debug(False)

@tool
def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["tyo", "tokyo", "东京"]:
        return location + "->" + "下雨"
    else:
        return location + "->" + "晴天"

@tool
def get_coolest_cities():
    """Get a list of coolest cities"""
    return ["Tokyo", "New York", "Los Angeles"]

# 工具数组
tools = [get_weather, get_coolest_cities]
# 创建一个工具节点
tool_node = ToolNode(tools=tools)

# 创建一个带有工具的模型
model_with_tools = ChatOpenAI(model_name="gpt-4o", temperature=0).bind_tools(tools)

# 调用模型执行用户请求
result = model_with_tools.invoke(input="请告诉我东京的天气？")
pprint.pprint(type(result))  # AIMessage

# 执行结果是返回工具调用请求(说明LLM无法处理用户的请求，需要调用工具)
pprint.pprint(result.tool_calls)
"""
[{'args': {'location': 'Tokyo'},
  'id': 'call_b7DWLNYHzI9wdCk6iNTOUfDZ',
  'name': 'get_weather',
  'type': 'tool_call'}]
"""

# 执行工具调用
result = tool_node.invoke({"messages": [result]})
pprint.pprint(result)
"""
{'messages': [ToolMessage(content='Tokyo->下雨', name='get_weather', tool_call_id='call_b7DWLNYHzI9wdCk6iNTOUfDZ')]}
"""
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

