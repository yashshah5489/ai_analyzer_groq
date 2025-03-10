import chromadb

class ChromaVectorStore:
    def __init__(self, collection_name="financial_docs"):
        # Initialize the client without persistence parameters
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_documents(self, ids, documents, metadatas=None):
        if metadatas is None:
            metadatas = [{}] * len(documents)
        self.collection.add(ids=ids, documents=documents, metadatas=metadatas)

    def query(self, query_text: str, n_results: int = 3):
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        return results.get("documents", [[]])[0]
