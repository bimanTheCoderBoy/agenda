from langchain_tavily import TavilySearch

search_tool = TavilySearch(max_results=5, max_depth="basic")