from pathlib import Path

from langchain_community.document_loaders import UnstructuredMarkdownLoader, UnstructuredWordDocumentLoader

SAMPLE_PATH = Path(__file__).resolve().parents[3] / "day03-code" / "assets" / "sample.docx"

document = UnstructuredWordDocumentLoader(
    file_path=str(SAMPLE_PATH),
    mode="single"
).load()
print(document)

print("*" * 50)

documents = UnstructuredWordDocumentLoader(
    file_path=str(SAMPLE_PATH),
    mode="elements"
).load()
for document in documents:
    print(document)