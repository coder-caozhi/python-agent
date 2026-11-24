from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel(model_name_or_path="../../assets/models/bge-m3")

result = model.encode(
    sentences="向量为辅、最大序列长度",
    return_dense=True, # 生成稠密向量
    return_sparse=True # 生成稀疏向量
)

print("稠密向量：")
print(result["dense_vecs"])

print("稀疏向量：")
print(result["lexical_weights"])

print("将稀疏向量传唤为关键字")
print(model.convert_id_to_token(result["lexical_weights"]))
