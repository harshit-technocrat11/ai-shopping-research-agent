import os
from langgraph.graph import StateGraph, START, END
from state import ShoppingState
from nodes.search import search_node
from nodes.evaluator import eval_node
from nodes.traffic_node import route_after_eval
from nodes.orchestrator import orchestrator_node
from nodes.worker import worker_node
from nodes.orchestrator import assign_workers
from nodes.aggregator import aggregator_node
from checkpointer import get_checkpointer


# define state workflow
workflow =  StateGraph(ShoppingState)

# add nodes
workflow.add_node("search", search_node)
workflow.add_node("eval_node", eval_node);
workflow.add_node("orchestrator_node", orchestrator_node)
workflow.add_node("worker_node", worker_node)
workflow.add_node("aggregator_node", aggregator_node)

# add edges 
workflow.add_edge(START , "search")
workflow.add_edge("search", "eval_node")

workflow.add_conditional_edges(

    "eval_node", #source node
    route_after_eval,  # condition func/ route

    {    # path map -which path to take , based on the function
        # after_eval_route() return value
        "search": "search",
        "orchestrator":"orchestrator_node"

    }
)
workflow.add_conditional_edges(
    "orchestrator_node",
    assign_workers,
    ["worker_node"] 
)

workflow.add_edge("worker_node", "aggregator_node")
workflow.add_edge("aggregator_node", END)

# memory
memory = get_checkpointer()

# compile
app = workflow.compile(checkpointer=memory)





