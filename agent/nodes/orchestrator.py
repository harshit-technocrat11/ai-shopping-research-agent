from langgraph.types import Send
from state import ShoppingState

# Send = message packet 

def orchestrator_node(state):
    """"
    Pick the top 5 URLs and store them in the state 
    so the workers know what to grab.
    """
    urls = [r["url"] for r in state["search_results"] if r.get("url")][:5]


    print(f"🎯 Orchestrator: Found {len(urls)} target URLs. Preparing workers...")

    # state update with list of URLS to scrape

    return {"urls_to_scrape": urls}

def assign_workers( state:ShoppingState):
    """
        this func acts as trigger for parallel exec of worker nodes. 
    """
    # 1. checking for urls
    urls = state.get("urls_to_scrape", [])
  
    # <worker node> url  
    
    return [Send("worker_node",{"url":url})
            for url in urls]
