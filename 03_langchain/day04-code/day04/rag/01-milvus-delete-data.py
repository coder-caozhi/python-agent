from pymilvus import MilvusClient

# 1. 创建连接
def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")

# 2. 删除实体
def delete_demo(client):
    result = client.delete(
        collection_name="demo_collection",
        filter = "id in [467901374367220713, 467901374367220714]"
    )
    print(result)

if __name__ == '__main__':

    client = get_milvus_client()
    delete_demo(client)

