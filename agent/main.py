from graph import app

# running it
if __name__ == "__main__":
    inputs = {"query": "best budget mechanical keyboard 2026, under 4000 INR"}
    result = app.invoke(inputs)
    print("\n--- Final State Results ---")
    for r in result["search_results"]:
        print(f"Title: {r['title']}\nURL: {r['url']}\n")