from langchain_community.embeddings import HuggingFaceEmbeddings

embed_model = HuggingFaceEmbeddings(
    model_name="../../assets/models/bge-base-zh-v1.5"
)

# 单文本嵌入
result = embed_model.embed_query("床前明月光 day day up")
print(result)
print(len(result))

# 批量文本转换
result = embed_model.embed_documents(["床前明月光", "疑是地上霜"])
for r in result:
    print(r)
