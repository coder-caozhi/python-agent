from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen:4b-instruct",
    base_url="http://127.0.0.1:11434"
)

result = llm.invoke("给我讲个笑话")

print(result)