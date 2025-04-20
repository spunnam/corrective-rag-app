from llama_index.core import SimpleDirectoryReader


def load_documents_from_directory(directory_path: str):
    """Loads documents using LlamaIndex's SimpleDirectoryReader."""
    reader = SimpleDirectoryReader(input_dir=directory_path)
    return reader.load_data()
