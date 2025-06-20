from langgraph.graph import StateGraph, add_messages, END
from langchain_core.messages import AIMessage, HumanMessage
from schema import AgentState
from langgraph.checkpoint.sqlite import SqliteSaver
from nodes.planning import planning_node
import sqlite3


sqlite_conn = sqlite3.connect("checkpoint.sqlite", check_same_thread=False)
memory = SqliteSaver(sqlite_conn)

# Define the state graph
graph=StateGraph(AgentState)






graph.add_node("planning", planning_node)


graph.set_entry_point("planning")





app = graph.compile(checkpointer=memory)

config = {"configurable": {
    "thread_id": 1
}}

result= app.invoke({
    "user_input": "Plan a trip to Paris",
    "chat_history": []
}, config=config)

print("Final result:", result)