from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse
import os

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        print(query)

        graph = GraphBuilder(model_provider="groq")
        react_app = graph()

        # Save graph image
        png_graph = react_app.get_graph().draw_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

        # Assuming request is a pydantic object like: {"question": "your text"}
        messages = {"messages": [query.query]}

        output = react_app.invoke(messages)

        # If result is dict with messages
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)

        return {"answer": final_output}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# -------------------------------
# Inside your GraphBuilder class
# -------------------------------

class GraphBuilder:
    def __init__(self, model_provider="groq"):
        self.model_provider = model_provider
        # self.tools = ...
        # self.agent_function = ...
        # self.graph = ...

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)

        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)

        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()