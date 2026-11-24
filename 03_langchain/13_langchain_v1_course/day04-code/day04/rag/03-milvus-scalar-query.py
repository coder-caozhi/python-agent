from pymilvus import MilvusClient

COLLECTION_NAME = "demo_collection"

def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")


def scalar_query_examples(client, like_keyword: str = "大模型"):
    # 对text字段进行检索
    like_res = client.query(
        collection_name=COLLECTION_NAME,
        filter=f'text like "%{like_keyword}%"',
        output_fields=["id", "text"],
        limit=5,
    )
    for row in like_res:
        print({"id": row.get("id"), "text": row.get("text")})

    print("----------------------")
    # 对metadata字段进行检索
    json_res = client.query(
        collection_name=COLLECTION_NAME,
        filter='metadata["source"] like "%sample%"',
        output_fields=["id", "metadata"],
        limit=5,
    )
    for row in json_res:
        print({"id": row.get("id"), "metadata": row.get("metadata")})


if __name__ == '__main__':
    client = get_milvus_client()
    scalar_query_examples(client, "责任")
