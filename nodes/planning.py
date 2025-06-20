from base_llm import llm
from langchain_core.output_parsers import PydanticOutputParser
from schema import AgentState, PlanOutput
from langchain.prompts import ChatPromptTemplate
from tools.tool import tools

plan_parser= PydanticOutputParser(pydantic_object=PlanOutput)

planning_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a task planning agent. Your job is to analyze user requests, break them into multiple steps, and for each step suggest which tool to use."),

    ("system", "Available tools: {tool_details}. If no tool is needed, set tool_hint to 'none'."),

    ("system", "Format output strictly as JSON:\n" + plan_parser.get_format_instructions().replace("{", "{{").replace("}", "}}")),

    ("human", "User request: {user_input}"),

    ("human", "Here is previous chat context:\n{chat_history}")
]).partial(
    tool_details="".join(f"{tool.name}: {tool.description}\n" for tool in tools)
)


def planning_node(state:AgentState) -> dict:
    """
    Planning node that generates a plan based on user input and chat history.
    """
    print("Planning node invoked with state:", state)
    prompt = planning_prompt.format_messages(
        user_input=state.user_input,
        chat_history=state.chat_history
    )
    print("Formatted planning prompt:", prompt)
    
    response = llm.invoke(prompt)

    print("Planning response:", response.content)
    
    plan_output = plan_parser.parse(response.content)
    print("Parsed plan output:", plan_output)

    return {"plan_json":plan_output, "chat_history": [response]}