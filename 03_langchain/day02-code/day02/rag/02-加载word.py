from langchain_community.document_loaders import UnstructuredMarkdownLoader, UnstructuredWordDocumentLoader

document = UnstructuredWordDocumentLoader(
    file_path="./assets/sample.docx",
    mode="single"
).load()
print(document)

print("*" * 50)

documents = UnstructuredWordDocumentLoader(
    file_path="./assets/sample.docx",
    mode="elements"
).load()
for document in documents:
    print(document)