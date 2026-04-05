from langgraph.types import Send

# Send = message packet 

def orchestrator_node(state):
    """"
    Pick the top 5 URLs and store them in the state 
    so the workers know what to grab.
    """


    print(f"🎯 Orchestrator: Found {len(urls)} target URLs. Preparing workers...")

    # state update with list of URLS to scrape

    return {"urls_to_scrap": urls}