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

# 笑话主题
class Subjects(BaseModel):
    subjects: list[str]

# 主图的整体状态
class OverallState(TypedDict):
    topic: str
    subjects: list[str]

####################################################################################################
## Nodes
# 这是我们用来生成笑话主题的函数
def generate_topics(state: OverallState):
    prompt = subjects_prompt.format(topic=state["topic"])
    response = model.with_structured_output(Subjects).invoke(prompt)
    return {"subjects": response.subjects}

####################################################################################################
## Graph
# 构建图：这里我们将所有内容放在一起构建我们的图
graph = StateGraph(OverallState)
graph.add_node("generate_topics", generate_topics)
graph.add_edge(START, "generate_topics")
graph.add_edge("generate_topics", END)

app = graph.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")

topic_title = "料理"
# 只返回结果
result = app.invoke({"topic": topic_title})
pprint.pprint(result)

print(evalEndTime(start_time))

