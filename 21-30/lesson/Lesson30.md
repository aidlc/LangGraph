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

# :books: 旁征博引的反思设计⑤ - 修正生成内容

操作步骤

+ 根据反思节点生成修正内容
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
    padding: 10px;
    background-color: white !important;
  }
</style>

# 系统架构

![width:100px](./images/Lesson30a.png)

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
### step1.py

```python
import pprint, json, datetime, warnings, common
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage
import step2, step3

warnings.simplefilter("ignore")

tavily_tool = TavilySearchResults(
    max_results=2,
)

# search_queries: AnswerQuestion 和 ReviseAnswer 的 search_queries 字段的值。
def run_queries(search_queries: list[str], **kwargs):
    """Run the generated queries."""

    print("+" * 100)
    pprint.pprint(search_queries)
    print("+" * 100)

    # 运行生成的查询。
    return tavily_tool.batch([{"query": query} for query in search_queries])

tool_node = ToolNode(
    [
        StructuredTool.from_function(run_queries, name=step2.AnswerQuestion.__name__),
        StructuredTool.from_function(run_queries, name=step3.ReviseAnswer.__name__),
    ]
)
```

---
<style scoped>
  h3 {
    margin-top: 0;
  }
  pre {
    box-shadow: 2px 2px 3px black;
  }
</style>
### step2.py

```python
import pprint, json, datetime, warnings, common
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field, ValidationError

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 反省点
class Reflection(BaseModel):

    # 对缺失部分的批评。
    missing: str = Field(description="Critique of what is missing.")

    # 对多余事物的批判
    superfluous: str = Field(description="Critique of what is superfluous")


# 回答问题。提供一个答案、反思，然后跟进搜索查询以改进答案。
class AnswerQuestion(BaseModel):
    """Answer the question. Provide an answer, reflection, and then follow up with search queries to improve the answer."""

    # "~250字详细回答问题"
    answer: str = Field(
        ...,
        description="~250 word detailed answer to the question.",
    )

    # “你对初步回答的反思。”
    reflection: Reflection = Field(
        ...,
        description="Your reflection on the initial answer.",
    )

    # “1-3个搜索查询，用于研究改进以解决当前答案的批评。”
    search_queries: list[str] = Field(
        ...,
        description="1-3 search queries for researching improvements to address the critique of your current answer.",
    )

actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert researcher.
Current time: {time}

1. Provide a detailed ~250 word answer.
2. Reflect and critique your answer. Be severe to maximize improvement.
3. Recommend search queries to research information and improve your answer.
""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        (
            "user",
            "Reflect on the user's original question and the"
            " actions taken thus far. Respond using the {function_name} function.",
        ),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
    function_name=AnswerQuestion.__name__,
)
initial_answer_chain = actor_prompt_template | llm.bind_tools(tools=[AnswerQuestion])
```

---
<style scoped>
  h3 {
    margin-top: 0;
  }
  pre {
    box-shadow: 2px 2px 3px black;
  }
</style>
### step3.py

```python
import pprint, json, datetime, warnings, common
import step2
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import Field
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class ReviseAnswer(step2.AnswerQuestion):
    """Revise your original answer to your question. Provide an answer, reflection,
    cite your reflection with references, and finally
    add search queries to improve the answer."""

    # 引用支持您更新后的答案。
    references: list[str] = Field(
        description="Citations motivating your updated answer."
    )

revisor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert researcher.
Current time: {time}

1. Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
2. Reflect and critique your answer. Be severe to maximize improvement.
3. Recommend search queries to research information and improve your answer.
""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        (
            "user",
            "Reflect on the user's original question and the"
            " actions taken thus far. Respond using the {function_name} function.",
        ),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
    function_name=ReviseAnswer.__name__,
)

revision_chain = revisor_prompt_template | llm.bind_tools(tools=[ReviseAnswer])
```

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

