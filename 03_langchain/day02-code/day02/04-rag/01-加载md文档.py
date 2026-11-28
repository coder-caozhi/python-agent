

from langchain_community.document_loaders import UnstructuredMarkdownLoader

# document = UnstructuredMarkdownLoader(
#     file_path="./assets/sample.md",
#     mode="single" # 默认值：加载完整文档
# ).load()
# print(document)


documents = UnstructuredMarkdownLoader(
    file_path="./assets/sample.md",
    mode="elements" # 按照标题切割,按正文段落切割
).load()

for document in documents:
    print(document)