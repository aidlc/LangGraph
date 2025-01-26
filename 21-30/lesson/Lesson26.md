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

# :books: 旁征博引的反思设计② - 结构化反思输出

操作步骤

+ 根据用户输入的问题，生成反思结构化输出
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
### step2.py

```python
import pprint, json, datetime, warnings, common
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# llm = ChatOpenAI(model="gpt-4o", temperature=0) # 结构化输出错误，需要个别对应

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field, ValidationError


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


"""
system:
你是一位专家研究员。
当前时间: {time}

1. 请提供一个详细的答案, 字数约为250字。
2. 反思并批判你的回答。要严格, 以最大限度地提升质量。
3. 建议一些搜索关键词来研究信息, 提升你的回答质量。

messages:

user:
请回顾用户的原始问题以及至今采取的操作。使用 {function_name} 函数进行回复。
"""
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
# LLM Chain
initial_answer_chain = actor_prompt_template | llm.bind_tools(tools=[AnswerQuestion])
# 验证器
validator = PydanticToolsParser(tools=[AnswerQuestion])
# 测试调用
response = initial_answer_chain.invoke(
    [HumanMessage(content="三国演义的桃园结义都是谁?")]
)
response.pretty_print()
# 结构化输出
result = validator.invoke(response)
print("=" * 100)
print(result)
# print("answer:", result[0].answer)
# print("reflection:", result[0].reflection)
# print("search_queries:", result[0].search_queries)
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

