from langchain_community.document_loaders import UnstructuredWordDocumentLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# 1. 加载文档
document = TextLoader(
    file_path="../../assets/sample.md",
    encoding="utf-8"
).load()

# 2. 切分文档
chunks = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "！", "？", "……", "，", ""],  # 分隔符列表
    chunk_size=100,  # 每个块的最大长度
    chunk_overlap=5,  # 每个块重叠的长度
    length_function=len,  # 可选：计算文本长度的函数，默认为字符串长度，可自定义函数来实现按 token 数切分
    add_start_index=True,  # 可选：块的元数据中添加此块起始索引
).split_documents(document)

for chunk in chunks:
    print("*" * 100)
    print(chunk.page_content)


