import os 
from dotenv import load_dotenv
from tavily import TavilyClient
from state import ShoppingState
load_dotenv()

client = TavilyClient(api_key=os.getenv("tavily_api"))

def search_node(state: ShoppingState):
    # state passed

    print(f"\n🔍 Searching: {state['query']}")  # streaming feel

    results = client.search(query=state["query"], max_results=4)
    # printing tavily results

    # print(results)

   # We return ONLY the keys we want to update in the state
    return {"search_results": results["results"]}