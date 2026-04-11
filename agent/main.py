import time
from langgraph.types import Command
from graph import app

# config: This Thread ID identifies this specific research session
# u can change this to start a fresh search or keep it to resume later

config = {"configurable": {"thread_id": "shopping_session_001"}}

def run_agent():
    inputs = {
        "query": "Im looking for the best electric guitars under 20k ",
        "search_retries": 0,
        "scraped_data": []
    }

    print("🚀 --- STARTING AI SHOPPING RESEARCH AGENT ---")
    
    # 1. First Execution: Runs until it hits the interrupt in aggregator_node
    # stream_mode="updates" lets us see each node as it finishes

    for event in app.stream(inputs, config=config, stream_mode="updates"):
        for node, data in event.items():
            print(f"\n✅ Finished Node: {node}")
            if node == "worker_node":
                print(f"   ⚙️  Successfully scraped a new source.")

    # 2. if interrupt occurs
    snapshot = app.get_state(config)

    if snapshot.next:
        print("\n" + "="*40)
        print("🛑 AGENT WAITING FOR USER FEEDBACK")
        print("="*40)
        print("The agent has gathered the research data.")
        user_feedback = input("\n💬 Any specific focus for the final report? (e.g., 'focus on hot-swappable keys'): ")

        # 3. Resume Execution: Sends the human input back to the aggregator
        print("\n✍️ Generating final report with your feedback...")
        for event in app.stream(
            Command(resume=user_feedback), 
            config=config, 
            stream_mode="updates"
        ):
            if "aggregator_node" in event:
                print("✅ Final Report synthesized.")

    # 4. Final Output Display
    final_state = app.get_state(config).values
    report = final_state.get("final_report")

    if report:
        print("\n" + "-"*40)
        print("📋 FINAL RESEARCH REPORT")
        print("-"*40)
        print(f"\n{report}")
    else:
        print("\n❌ Error: Report generation failed.")

if __name__ == "__main__":
    run_agent()