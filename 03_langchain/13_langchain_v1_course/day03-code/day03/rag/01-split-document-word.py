"""
RAG（Retrieval-Augmented Generation，检索增强生成）文档预处理示例
=============================================================

RAG 的核心流程：
  1. 文档加载（Load）      —— 将原始文件（Word/PDF/HTML 等）读取为 LangChain 的 Document 对象
  2. 文档切分（Split）     —— 将长文档切分成合适大小的文本块（Chunk），便于后续向量化
  3. 向量化（Embedding）   —— 将每个 Chunk 通过 Embedding 模型转换为向量
  4. 存入向量数据库（Store）—— 将向量存入 FAISS / Chroma / Milvus 等向量数据库
  5. 检索 + 生成（Retrieve & Generate）—— 用户提问时，检索最相关的 Chunk，拼入 Prompt 交给 LLM 回答

本文件演示的是前两步：加载 Word 文档 → 递归切分文本。
"""

from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==================== 第一步：加载文档 ====================
#
# UnstructuredWordDocumentLoader —— Word 文档加载器
# -------------------------------------------------------
# 底层依赖：python-docx（解析 .docx）和 unstructured 库（统一解析各类非结构化文件）
# 安装依赖：pip install python-docx unstructured langchain-community
#
# 参数说明：
#   file_path : str  —— 文档路径，支持 .doc / .docx 格式
#   mode : str       —— 加载模式，可选值：
#       "single"   : （默认）将整篇文档合并为一个 Document 对象，page_content 为全文文本
#       "elements" : 按段落/标题/表格等元素拆分，每个元素独立成一个 Document 对象
#       "paged"    : 按页拆分（如果文档有分页信息的话）
#
# 返回值：
#   .load() 返回 List[Document]，每个 Document 包含：
#     - page_content : str   —— 文本内容
#     - metadata     : dict  —— 元数据（如 source 文件路径等）
#
# 其他常用文档加载器：
#   PyPDFLoader           —— 加载 PDF
#   TextLoader            —— 加载纯文本
#   CSVLoader             —— 加载 CSV
#   UnstructuredHTMLLoader—— 加载 HTML
#   DirectoryLoader       —— 批量加载整个目录下的文件
#
document = UnstructuredWordDocumentLoader(
    file_path="../../assets/sample.docx",
    mode="single"
).load()

# ==================== 第二步：切分文档 ====================
#
# RecursiveCharacterTextSplitter —— 递归字符文本切分器（LangChain 推荐的通用切分器）
# -----------------------------------------------------------------------
# 核心思想：按 separators 列表中的分隔符从左到右（优先级从高到低）依次尝试切分，
#           优先在更大粒度的语义边界（段落 > 换行 > 句号 > 逗号）处断开，
#           从而最大程度保留文本块的语义完整性。
#
# 递归切分流程：
#   1. 先尝试用第一个分隔符（如 "\n\n"，双换行/段落）切分文本
#   2. 检查每个切分片段的长度是否 <= chunk_size
#   3. 如果某个片段仍然太长，则递归地用下一个分隔符继续切分
#   4. 最终如果所有分隔符都无法将文本切到 chunk_size 以内，就按单字符强制切断
#
# 参数详解：
#   separators   : List[str]
#       分隔符优先级列表，从左到右优先级递减。
#       本例适配中文文档：段落换行 → 单换行 → 句末标点（。！？……）→ 逗号 → 单字符
#       英文文档常用：["\n\n", "\n", " ", ""]
#
#   chunk_size   : int = 400
#       每个文本块的最大字符数上限。
#       选择依据：通常根据所用 Embedding 模型的 token 上限来定，
#       例如 OpenAI text-embedding-ada-002 最大支持 8191 tokens，
#       一般设为 500~1000 字符较为常见，太大检索精度下降，太小语义不完整。
#
#   chunk_overlap : int = 50
#       相邻两个 Chunk 之间的重叠字符数。
#       作用：防止关键信息恰好落在切分边界处被截断丢失，
#       通过保留前后文重叠来维持上下文的连贯性。
#       一般设为 chunk_size 的 10%~20%。
#
#   length_function : Callable = len
#       计算文本长度的函数，默认按字符数（len）。
#       进阶用法：可传入 tiktoken 的编码函数来按 token 数切分，例如：
#         import tiktoken
#         enc = tiktoken.encoding_for_model("gpt-4")
#         length_function = lambda text: len(enc.encode(text))
#
#   add_start_index : bool = True
#       是否在每个 Chunk 的 metadata 中记录其在原文档中的字符起始偏移量（start_index），
#       便于后续溯源定位原文位置。
#
# 其他常用切分器：
#   CharacterTextSplitter       —— 仅按单一分隔符切分（不递归）
#   TokenTextSplitter           —— 按 token 数切分
#   MarkdownHeaderTextSplitter  —— 按 Markdown 标题层级切分
#   HTMLHeaderTextSplitter      —— 按 HTML 标题标签切分
#   SpacyTextSplitter           —— 基于 spaCy NLP 的句子切分
#
chunks = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "！", "？", "……", "，", ""],  # 分隔符列表
    chunk_size=400,  # 每个块的最大长度
    chunk_overlap=50,  # 每个块重叠的长度
    length_function=len,  # 可选：计算文本长度的函数，默认为字符串长度，可自定义函数来实现按 token 数切分
    add_start_index=True,  # 可选：块的元数据中添加此块起始索引
).split_documents(document)

# ==================== 第三步：查看切分结果 ====================
#
# 每个 chunk 是一个 Document 对象，包含：
#   chunk.page_content  —— 该块的文本内容
#   chunk.metadata      —— 元数据字典，包含：
#     - "source"      : 原始文件路径
#     - "start_index" : 该块在原文中的字符起始位置（因 add_start_index=True）
#
for chunk in chunks:
    print("*" * 100)
    print(chunk.page_content)
