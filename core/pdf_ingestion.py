from llama_index.core import SimpleDirectoryReader


def load_documents_from_directory(directory_path: str):
    """Loads documents using LlamaIndex's SimpleDirectoryReader."""
    reader = SimpleDirectoryReader(input_dir=directory_path)
    docs = reader.load()
    print("Documents from reader->", print(len(docs)))
    for doc in docs:
        print("Doc=>", doc)
    return docs
