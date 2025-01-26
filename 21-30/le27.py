import pprint, json, datetime, warnings, common
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# llm = ChatOpenAI(model="gpt-4o", temperature=0)
# llm = ChatOpenAI(model="gpt-4", temperature=0)
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field, ValidationError


# 反省点
# class Reflection(BaseModel):

#     # 对缺失部分的批评。
#     missing: str = Field(description="Critique of what is missing.")

#     # 对多余事物的批判
#     superfluous: str = Field(description="Critique of what is superfluous")


# 回答问题。提供一个答案、反思，然后跟进搜索查询以改进答案。
class AnswerQuestion(BaseModel):
    """Answer the question. Provide an answer, reflection, and then follow up with search queries to improve the answer."""

    # "~250字详细回答问题"
    answer: str = Field(
        ...,
        description="~250 word detailed answer to the question.",
    )

    # “你对初步回答的反思。”
    # reflection: Reflection = Field(
    #     ...,
    #     description="Your reflection on the initial answer.",
    # )

    # 对缺失部分的批评。
    reflection_missing: str = Field(description="Critique of what is missing.")

    # 对多余事物的批判
    reflection_superfluous: str = Field(description="Critique of what is superfluous")

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
请回顾用户的原始问题以及至今采取的操作。
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
            " actions taken thus far.",
        ),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)

initial_answer_chain = actor_prompt_template | llm.with_structured_output(
    AnswerQuestion
)
response = initial_answer_chain.invoke(
    [HumanMessage(content="三国演义的桃园结义都是谁?")]
)
print(type(response))
print(response)
# print("\nanswer", "->", response.answer)
# print("\nreflection_missing", "->", response.reflection_missing)
# print("\nreflection_superfluous", "->", response.reflection_superfluous)
# print("\nsearch_queries", "->", response.search_queries)