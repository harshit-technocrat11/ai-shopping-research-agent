from langgraph.graph import StateGraph, START, END
from state import ShoppingState
from nodes.search import search_node

# define state workflow
workflow =  StateGraph(ShoppingState)

# add nodes
workflow.add_node("search", search_node)

# add edges 
workflow.add_edge(START , "search")
workflow.add_edge("search", END)


# compile
app= workflow.compile()

# running it
if __name__ == "__main__":
    inputs = {"query": "best budget mechanical keyboard 2026, under 4000 INR"}
    result = app.invoke(inputs)
    print("\n--- Final State Results ---")
    for r in result["search_results"]:
        print(f"Title: {r['title']}\nURL: {r['url']}\n")