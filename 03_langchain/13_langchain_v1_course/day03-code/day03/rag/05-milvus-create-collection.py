from pprint import pprint

from pymilvus import MilvusClient, DataType

# 1. 创建连接
def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")

# 2. 创建字段
def build_schema():

    # 返回 schema
    return MilvusClient.create_schema(
        auto_id = True,
    ).add_field(#主键
        field_name="id",
        datatype=DataType.INT64,
        is_primary=True,
    ).add_field( #稠密向量
        field_name="vector",
        datatype=DataType.FLOAT_VECTOR,
        dim=1024
    ).add_field(#稀疏向量
        field_name="sparse_vector",
        datatype=DataType.SPARSE_FLOAT_VECTOR
    ).add_field(
        field_name="text", # 原始的chunk
        datatype=DataType.VARCHAR,
        max_length=1000
    ).add_field(
        field_name="metadata", # 元数据
        datatype=DataType.JSON
    )

# 3. 创建索引
def create_index():

    # 获取索引对象
    index_params = MilvusClient.prepare_index_params()

    # 创建稠密向量的索引
    index_params.add_index(
        field_name="vector",
        index_type="HNSW",
        metric_type="L2"
    )

    # 创建稀疏向量的索引
    index_params.add_index(
        field_name="sparse_vector",
        index_type="SPARSE_INVERTED_INDEX",
        metric_type="IP"
    )

    # 返回索引对象
    return index_params

# 4. 创建集合
def create_collection(client: MilvusClient, collection_name):

    client.create_collection(
        collection_name=collection_name,
        schema=build_schema(),
        index_params=create_index()
    )


if __name__ == '__main__':

    # 1. 获取链接对象
    client = get_milvus_client()

    # 2. 创建集合
    create_collection(client, "demo_collection")

    # 3. 打印输出
    print(client.list_collections())
    pprint(client.describe_collection(collection_name="demo_collection"))