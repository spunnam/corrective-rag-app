import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.core.schema import Document


def init_vector_store(
    host: str = "localhost", port: int = 6333, collection_name: str = "test"
) -> QdrantVectorStore:
    print("Initializing vector store")
    client = qdrant_client.QdrantClient(host=host, port=port)
    return QdrantVectorStore(client=client, collection_name=collection_name)


def init_embedding_model(
    model_name: str = "BAAI/bge-large-en-v1.5",
) -> FastEmbedEmbedding:
    print("Initializing Embed model")
    embed_model = FastEmbedEmbedding(model_name=model_name)
    Settings.embed_model = embed_model
    return embed_model


def create_index_from_documents(
    documents: list[Document], vector_store: QdrantVectorStore
) -> VectorStoreIndex:
    print("Creating Embeddings in create_index_from_documents")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_documents(documents, storage_context=storage_context)
