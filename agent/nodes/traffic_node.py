# graph router - after evaluation

def route_after_eval(state):
    # traffic control- to workers

    if state["eval_passed"]:
        return "orchestrator"  #target node name
    
    else :
        return "search"  #back track
    