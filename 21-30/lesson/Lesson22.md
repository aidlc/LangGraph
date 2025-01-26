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

# :books: 反应代理(ReAct Agent) - 使用互联网工具

操作步骤

+ 自定义互联网查询工具，使用代理从互联网上获取数据
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
import time, re
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain import globals
from bs4 import BeautifulSoup
import common

# 输出详细的调试信息
# globals.set_debug(True)

start_time = time.time()  # 获取开始时间

@tool
def scrape_web(url: str):
    """This tool is used to scrape the web. It takes a URL as input and returns the text content of the page."""

    print("Scraping URL:", url)

    def bs4_extractor(html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        main_contents = soup.find("body")
        content = re.sub(r"\n\n+", "\n\n", main_contents.text).strip()
        # print(content)
        return content

    return RecursiveUrlLoader(
        url,
        max_depth=1,
        # use_async=True,
        extractor=bs4_extractor,
        # metadata_extractor=None,
        # exclude_dirs=(),
        # timeout=10,
        # check_response_status=True,
        continue_on_failure=True,
        # prevent_outside=True,
        # base_url=None,
        # ...
    ).load()

# 工具数组
tools = [scrape_web]
tool_node = ToolNode(tools=tools)
# LLM模型
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# 创建一个与利用工具调用的图表代理
system_prompt = (
    "你是一名有用的AI助手, 你会在必要时使用互联网工具收集信息, 并完美地回答用户的问题。"
)
agent = create_react_agent(model=model, tools=tools, state_modifier=system_prompt)
# agent.get_graph().draw_mermaid_png(output_file_path="graph.png")

# 用户提示词
messages = {
    "messages": [
        (
            "human",
            """
帮我总结一下这个网页的内容, 要求在200个字以内。

url:https://medium.com/@cplog/introduction-to-langgraph-a-beginners-guide-14f9be027141
""",
        )
    ]
}
# https://medium.com/@tusharbosamiya1410/amazon-web-service-lambda-service-b7ea3a956f50

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

