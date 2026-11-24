from pathlib import Path

from langchain_community.document_loaders import UnstructuredMarkdownLoader

SAMPLE_PATH = Path(__file__).resolve().parents[3] / "day03-code" / "assets" / "sample.md"

# document = UnstructuredMarkdownLoader(
#     file_path=str(SAMPLE_PATH),
#     mode="single" # 默认值：加载完整文档
# ).load()
# print(document)


documents = UnstructuredMarkdownLoader(
    file_path=str(SAMPLE_PATH),
    mode="elements" # 按照标题切割,按正文段落切割
).load()

for document in documents:
    print(document)