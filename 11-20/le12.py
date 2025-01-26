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
best_joke_prompt = """以下是一些关于{topic}的笑话。请选择最好的一条！返回最好笑话的编号。

{jokes}"""

# 笑话主题
class Subjects(BaseModel):
    subjects: list[str]

# 笑话
class Joke(BaseModel):
    joke: str

# 最好的笑话ID
class BestJoke(BaseModel):
    id: int

# 主图的整体状态
class OverallState(TypedDict):
    # 主题
    topic: str
    # 主题列表
    subjects: list[str]
    # 笑话列表
    jokes: Annotated[list, operator.add]
    # 最好的笑话
    best_selected_joke: str

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

# 选出最好的笑话
def best_joke(state: OverallState):
    jokes = "\n\n".join(state["jokes"])
    prompt = best_joke_prompt.format(topic=state["topic"], jokes=jokes)
    response = model.with_structured_output(BestJoke).invoke(prompt)
    return {"best_selected_joke": state["jokes"][response.id - 1]}

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
graph.add_node("best_joke", best_joke)
graph.add_edge(START, "generate_topics")
graph.add_conditional_edges("generate_topics", continue_to_jokes, ["generate_joke"])
graph.add_edge("generate_joke", "best_joke")
graph.add_edge("best_joke", END)

app = graph.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")

topic_title = "料理"
# 只返回结果
result = app.invoke({"topic": topic_title})
pprint.pprint(result)

print(evalEndTime(start_time))