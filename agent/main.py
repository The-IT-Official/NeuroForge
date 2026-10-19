from fastapi import FastAPI
from pydantic import BaseModel
from graph import app as agent
from langchain_core.messages import HumanMessage

api = FastAPI()

class Query(BaseModel):
    query: str

@api.post("/chat")
async def chat(query: Query):
    result = []
    for chunk in agent.stream({"messages": [HumanMessage(content=query.query)]}):
        for node, values in chunk.items():
            msg = values["messages"][-1]
            if msg.content:
                result.append({"node": node, "content": msg.content})
    return {"response": result}
