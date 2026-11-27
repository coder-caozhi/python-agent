# 1. 创建连接
from FlagEmbedding import BGEM3FlagModel
# from langchain_community.chat_models.openai import ChatOpenAI
from pymilvus import MilvusClient, AnnSearchRequest, RRFRanker, WeightedRanker

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 加载配置
load_dotenv(override=True)


def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")


# 2. 将问题转换成向量
def query_to_vector(query: str):
    model = BGEM3FlagModel(model_name_or_path="../../assets/models/bge-m3")
    result = model.encode(
        sentences=query,
        return_dense=True,  # 生成稠密向量
        return_sparse=True  # 生成稀疏向量
    )
    return result["dense_vecs"], result["lexical_weights"]

# 3. 稠密向量检索
def dense_vector_search_data(client: MilvusClient, query: str):
    dense_vector, _ = query_to_vector(query)
    result = client.search(
        collection_name="demo_collection",
        anns_field="vector",
        data=[dense_vector],
        limit=3,
        search_params={"metric_type": "L2"}, # 相似度的计算方式，与构建索引时一致
        output_fields=["id", "text", "metadata"] # 检索的结果中包含的字段
    )
    print(result)


# 4. 稀疏向量检索
def sparse_vector_search_data(client: MilvusClient, query: str):
    _, sparse_vector = query_to_vector(query)
    result = client.search(
        collection_name="demo_collection",
        anns_field="sparse_vector",
        data=[sparse_vector],
        limit=3,
        search_params={"metric_type": "IP"}, # 相似度的计算方式，与构建索引时一致
        output_fields=["id", "text", "metadata"] # 检索的结果中包含的字段
    )
    print(result)


# 5. 混合搜索
def hybrid_search_data(client: MilvusClient, query: str):

    # 1. 向量转换
    dense_vector, sparse_vector = query_to_vector(query)

    # 2. 定义稠密向量的混合搜索请求对象
    dense_vector_req = AnnSearchRequest(
        data = [dense_vector],
        anns_field="vector",
        param={"metric_type": "L2"},
        limit=5
    )

    # 3. 定义稀疏向量的混合搜索请求对象
    sparse_vector_req = AnnSearchRequest(
        data=[sparse_vector],
        anns_field="sparse_vector",
        param={"metric_type": "IP"},
        limit=5
    )

    # 4. 执行混合搜索
    result= client.hybrid_search(
        collection_name="demo_collection",
        reqs=[dense_vector_req, sparse_vector_req],
        output_fields=["id", "text", "metadata"],
        limit=5,
        # ranker=WeightedRanker(0.8, 0.3)
        ranker=RRFRanker() # 设置混合向量的重排序方式
    )

    print(result)

    return result

# 6. 生成答案
def generate_answer(client: MilvusClient, query: str):
    rag_results = hybrid_search_data(client, query)
    context = "\n".join([i['entity']['text'] for i in rag_results[0]])

    llm = ChatOpenAI(
        model="deepseek-v4-pro"
    )

    result = llm.invoke([
        ("system", "你是一个专业的法律顾问"),
        ("user", f"请根据上下文和用户问题进行总结。\n上下文:{context}\n用户的问题:{query}")
    ])

    print(result.content)


if __name__ == '__main__':
    client = get_milvus_client()
    # dense_vector_search_data(client, "监护人应该履行什么职责")
    # sparse_vector_search_data(client, "监护人应该履行什么职责")
    # hybrid_search_data(client, "监护人应该履行什么职责")
    generate_answer(client, "监护人应该履行什么职责")
