from langchain_community.document_loaders import UnstructuredWordDocumentLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import MilvusClient
from FlagEmbedding import BGEM3FlagModel


# 1. 创建连接
def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")

# 2. 批量插入数据
def insert_data(client: MilvusClient, collection_name):
    # 1. 加载word文档
    # document = UnstructuredWordDocumentLoader(
    #     file_path="../../assets/sample.docx",
    #     mode="single"
    # ).load()
    document = TextLoader(
        file_path="../../assets/sample.md",
        encoding="utf-8"
    ).load()

    # 2. 切分文档
    chunks = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "！", "？", "……", "，", ""],  # 分隔符列表
        chunk_size=400,  # 每个分块的大小
        chunk_overlap=20  # 分块之间的重叠部分
    ).split_documents(document)

    chunks = chunks[0:20]

    # 3. 构建稠密向量和稀疏向量
    model = BGEM3FlagModel(model_name_or_path="../../assets/models/bge-m3")
    all_vectors = model.encode(
        sentences=[chunk.page_content for chunk in chunks],
        return_dense=True,  # 生成稠密向量
        return_sparse=True  # 生成稀疏向量
    )
    dense_vectors = all_vectors["dense_vecs"]
    sparse_vectors = all_vectors["lexical_weights"]

    # 4. 组装数据列表
    data_list = []

    result = zip(chunks, dense_vectors, sparse_vectors)

    for chunk, dense_vector, sparse_vector in result:
        data_list.append({
            "text": chunk.page_content,
            "vector": dense_vector,
            "sparse_vector": sparse_vector,
            "metadata": chunk.metadata
        })

    # 5. 插入数据
    client.insert(collection_name=collection_name, data=data_list)

if __name__ == '__main__':

    client = get_milvus_client()
    insert_data(client, "demo_collection")