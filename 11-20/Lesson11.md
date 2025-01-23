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

# :books: 最好的笑话 - 并行生成笑话

操作步骤

+ 根据上期生成的主题，并行生成笑话

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
    background-color: white !important;
    padding: 20px;
  }
</style>

# 系统架构

![width:180px](./images/Lesson10a.png)

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
import pprint, time
import operator
from typing import Annotated, TypedDict
from common import evalEndTime
from langchain_core.pydantic_v1 import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.constants import Send
from langgraph.graph import END, StateGraph, START
from dotenv import load_dotenv

print("=" * 100)
start_time = time.time()  # 获取开始时间
load_dotenv()  # 读取.env文件

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.8)

subjects_prompt = """生成 5 个与 {topic} 相关的关键字，并用逗号分隔。"""
joke_prompt = """编一个关于{subject}的中文笑话"""

# 笑话主题
class Subjects(BaseModel):
    subjects: list[str]

# 笑话
class Joke(BaseModel):
    joke: str

# 主图的整体状态
class OverallState(TypedDict):
    # 主题
    topic: str
    # 主题列表
    subjects: list[str]
    # 笑话列表
    jokes: Annotated[list, operator.add]

# 笑话节点状态（生成一个笑话）
class JokeState(TypedDict):
    subject: str

####################################################################################################
## Nodes
# 这是我们用来生成笑话主题的函数
def generate_topics(state: OverallState):
    prompt = subjects_prompt.format(topic=state["topic"])
    response = model.with_structured_output(Subjects).invoke(prompt)
    return {"subjects": response.subjects}

# 这是我们根据主题生成笑话的地方
def generate_joke(state: JokeState):
    prompt = joke_prompt.format(subject=state["subject"])
    response = model.with_structured_output(Joke).invoke(prompt)
    return {"jokes": [response.joke]}

####################################################################################################
## Edges

# 定义遍历生成的主题的逻辑(条件边)
def continue_to_jokes(state: OverallState):
    # 遍历所有主题，导向到生成笑话的节点
    return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]

####################################################################################################
## Graph
# 构建图：这里我们将所有内容放在一起构建我们的图
graph = StateGraph(OverallState)
graph.add_node("generate_topics", generate_topics)
graph.add_node("generate_joke", generate_joke)
graph.add_edge(START, "generate_topics")
graph.add_conditional_edges("generate_topics", continue_to_jokes, ["generate_joke"])
graph.add_edge("generate_joke", END)

app = graph.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")

topic_title = "料理"
# 只返回结果
result = app.invoke({"topic": topic_title})
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

