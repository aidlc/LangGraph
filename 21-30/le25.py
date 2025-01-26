import pprint, json, datetime, warnings, common
from langchain_community.tools.tavily_search import TavilySearchResults
warnings.simplefilter("ignore")

tavily_tool = TavilySearchResults(
    max_results=2,
    # include_answer=True,
    # include_raw_content=True,
    # include_images=True,
    # search_depth="advanced",
    # include_domains = []
    # exclude_domains = []
)
results = tavily_tool("苹果公司的创始人是谁？")
pprint.pprint(results)