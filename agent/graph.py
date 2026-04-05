from langgraph.graph import StateGraph, START, END
from state import ShoppingState
from nodes.search import search_node
from nodes.evaluator import eval_node
from nodes.traffic_node import route_after_eval


# define state workflow
workflow =  StateGraph(ShoppingState)

# add nodes
workflow.add_node("search", search_node)
workflow.add_node("eval_node", eval_node);
workflow.add_node("orchestrator", orchestrator)

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



# compile
app= workflow.compile()





