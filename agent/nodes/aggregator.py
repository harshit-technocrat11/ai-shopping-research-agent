from langgraph.types import interrupt
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

def aggregator_node(state): 
    # format- gathered data from workers

    combined_research = "\n\n".join(
        [f"SOURCE: {d['url']}\nSUMMARY: {d['summary']}" for d in state["scraped_data"]]
    )

    print(f"📊 Aggregating {len(state['scraped_data'])} research summaries...")

    # human - in -loop interrupt : feedback
    feedback = interrupt(
        f"I have researched from {len(state["scraped_data"])} sources. "
        "Is there any specific detail (like battery, price, color, or warranty) I should emphasize?"
    )
    

    # final prompt
    prompt = (
        "You are a smart shopping shopping research assistant- you job is to filter out the data you recieve , in order to answer the user query , saving their time."
        f"Query: {state['query']}\n"
        f"User Feedback: {feedback}\n\n"
        f"Research Data:\n{combined_research}\n\n"
        "Please write a concise shopping report from the data, ( yet covering all the details ) "
        "Include a 'Best Value' and 'Top Pick' section with reasoning."
    )
    
    report = llm.invoke(prompt)
    
    return {"final_report": report.content}