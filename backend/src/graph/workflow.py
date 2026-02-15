from langgraph.graph import StateGraph, START, END
from backend.src.graph.states import VideoAuditState
from backend.src.graph.nodes import (
    index_video_node,
    compliance_auditor
)

def create_graph():

    workflow = StateGraph(VideoAuditState)

    # Adding Nodes
    workflow.add_node("indexer", index_video_node)
    workflow.add_node("auditor", compliance_auditor)

    # Adding Edges
    workflow.add_edge(START, "indexer")
    workflow.add_edge("indexer", "auditor")
    workflow.add_edge("auditor", END)

    # Compile the Graph
    app = workflow.compile()

    return app

app = create_graph()
