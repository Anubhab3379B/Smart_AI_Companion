import os
from typing import List, Optional
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

class MemorySystem:
    """
    Manages the RAG system using ChromaDB and Sentence Transformers.
    """
    def __init__(self, persistence_dir: str = "chroma_db", embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the MemorySystem.

        Args:
            persistence_dir (str): Directory to save ChromaDB data.
            embedding_model (str): Name of the Hugging Face embedding model.
        """
        self.persistence_dir = persistence_dir
        self.embedding_function = SentenceTransformerEmbeddings(model_name=embedding_model)
        self.vector_store = Chroma(
            persist_directory=self.persistence_dir,
            embedding_function=self.embedding_function
        )
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def ingest_documents(self, source_path: str) -> None:
        """
        Ingests documents from a file or directory.

        Args:
            source_path (str): Path to a file or directory.
        """
        documents: List[Document] = []
        
        if os.path.isfile(source_path):
            if source_path.endswith(".pdf"):
                loader = PyPDFLoader(source_path)
                documents.extend(loader.load())
            elif source_path.endswith(".txt") or source_path.endswith(".md"):
                loader = TextLoader(source_path)
                documents.extend(loader.load())
        elif os.path.isdir(source_path):
            # Load PDFs
            pdf_loader = DirectoryLoader(source_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
            documents.extend(pdf_loader.load())
            # Load Text
            txt_loader = DirectoryLoader(source_path, glob="**/*.txt", loader_cls=TextLoader)
            documents.extend(txt_loader.load())
        
        if not documents:
            print(f"No documents found in {source_path}")
            return

        splits = self.text_splitter.split_documents(documents)
        self.vector_store.add_documents(splits)
        # self.vector_store.persist() # Chroma 0.4+ persists automatically
        print(f"Ingested {len(splits)} chunks.")

    def query(self, query: str, k: int = 3) -> List[Document]:
        """
        Retrieves relevant documents for a query.

        Args:
            query (str): The search query.
            k (int): Number of results to return.

        Returns:
            List[Document]: List of relevant documents.
        """
        return self.vector_store.similarity_search(query, k=k)

if __name__ == "__main__":
    # Example usage
    # mem = MemorySystem()
    # mem.ingest_documents("my_notes.txt")
    # results = mem.query("What is quantum entanglement?")
    # for doc in results:
    #     print(doc.page_content)
    pass
