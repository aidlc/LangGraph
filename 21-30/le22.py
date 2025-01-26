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