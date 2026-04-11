# using gpt-4o-mini

from langchain_openai import ChatOpenAI
from bs4 import BeautifulSoup
import httpx

worker_llm =  ChatOpenAI(model="gpt-4o-mini", temperature=0)

def worker_node(state):
    url = state['url']
    print(f"worker into action: {url}")

    try:
        # 1. Fetch
        res = httpx.get(url, timeout=10, follow_redirects=True)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # 2. Cleaning
        content = soup.get_text(separator=" ", strip=True)[:4000] 
        
        # 3. Extract
        prompt = f"Extract product name, price, and top 2 pros/cons from this text:\n\n{content}"
        summary = worker_llm.invoke(prompt)
        
        return {"scraped_data": [{"url": url, "summary": summary.content}]}
        
    except Exception as e:
        return {"scraped_data": [{"url": url, "summary": f"Error: {str(e)}"}]}