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

# :books: 反思代理设计 - 反思一下《卖火柴的小女孩》

操作步骤

+ 编写一片《卖火柴的小女孩》的文章，并自动反思修改文章
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
import pprint, time, random, operator
from typing import List, TypedDict, Optional, Annotated, Dict, Literal
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END, MessageGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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

generation_prompt = ChatPromptTemplate(
    [
        SystemMessage(
            (
                "你是一名论文助手，任务是撰写优秀的五段式论文。"
                "根据用户的要求，生成最佳的论文。"
                "如果用户提出批评，请根据你之前的尝试提供修改后的版本。"
            )
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
generation_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)
generation_chain = generation_prompt | generation_llm

def generation(state):
    print("---", generation_name, "---")
    # print(generation_prompt.format(messages=state))
    result = generation_chain.invoke({"messages": state})
    return [result]

reflection_prompt = ChatPromptTemplate(
    [
        SystemMessage(
            (
                "你是一位正在批改作文的老师。请对用户提交的作文进行批评和建议。"
                "请提供详细的建议，包括对篇幅、深度、风格等方面的要求，让对方继续修改文章。"
            )
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
reflection_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)
reflection_chain = reflection_prompt | reflection_llm

def reflection(state):
    print("---", reflection_name, "---")
    # 将AI生成的文章作为人类的输入，然后让AI进行反思和指摘
    last_ai_message = [msg for msg in state if isinstance(msg, AIMessage)][-1]
    result = reflection_chain.invoke(
        {
            "messages": [
                HumanMessage(content=state[0].content),  # 用户原始输入
                HumanMessage(content=last_ai_message.content),  # AI生成的文章
            ]
        }
    )
    # 反思节点返回的是一个人类消息，模拟人类对AI生成的内容进行反思和指摘
    return [HumanMessage(content=result.content)]

####################################################################################################
## Edges
# 构建边：这里我们将构建流图的边
def condition_function(state):
    print("---", "condition_function", "---")
    ai_messages = [msg for msg in state if isinstance(msg, AIMessage)]
    if len(ai_messages) >= 2:
        return END
    else:
        return reflection_name

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
    HumanMessage(
        f"写一篇文章，解释为什么《卖火柴的小女孩》对现代儿童仍然具有重要意义。"
    ),
]

result = app.invoke(messages)
print("-" * 100)
for msg in result:
    print(msg.content)
    print("-" * 100)

# 流式输出（同时标识消息类型）
# events = app.stream(
#     messages,
#     stream_mode="values",
# )
# for i, step in enumerate(events):
#     print(f"Step {i}")
#     step[-1].pretty_print()

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

