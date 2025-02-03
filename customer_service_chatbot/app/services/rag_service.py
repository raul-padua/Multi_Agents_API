import logging
import os
import chromadb
import openai
from chromadb.utils import embedding_functions
from llama_index.core import SimpleDirectoryReader
from config import OPENAI_API_KEY

# Setup logging
logging.basicConfig(level=logging.INFO, format="🔹 %(message)s")
logger = logging.getLogger(__name__)

class RAGPolicyRetriever:
    """Retrieves policies dynamically using ChromaDB-based similarity search."""

    def __init__(self, policy_dir="app/policies/retrievable/"):
        self.policy_dir = policy_dir
        self.db_path = "chroma_db"
        self.collection_name = "policy_embeddings"

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=self.db_path)

        # Ensure the collection exists
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

        # Initialize OpenAI API client
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

        self.documents = []

    def load_policies(self):
        """Loads policies from .txt files into memory and removes empty ones."""
        self.documents = []
        reader = SimpleDirectoryReader(input_dir=self.policy_dir)
        docs = reader.load_data()

        # Filter out empty policies
        self.documents = [doc.text.strip() for doc in docs if doc.text.strip()]

        logger.info(f"✅ Loaded {len(self.documents)} policy documents after filtering empty files.")

    def create_vector_store(self):
        """Creates ChromaDB vector store from policies."""
        if not self.documents:
            raise ValueError("No policies found. Run `load_policies()` first.")

        stored_data = self.collection.get(include=["documents"])
        if stored_data and "documents" in stored_data and stored_data["documents"]:
            logger.warning(f"⚠️ ChromaDB already contains {len(stored_data['documents'])} policies. Skipping reinsertion.")
            return

        doc_ids = [f"policy_{i}" for i in range(len(self.documents))]

        try:
            logger.info(f"🟡 Sending {len(self.documents)} policies to OpenAI embeddings API")

            embeddings_response = self.openai_client.embeddings.create(
                input=self.documents,
                model="text-embedding-ada-002"
            )

            vector_embeddings = [data.embedding for data in embeddings_response.data]

            self.collection.add(
                ids=doc_ids,
                documents=self.documents,
                embeddings=vector_embeddings
            )

            logger.info(f"🟢 ChromaDB now contains {len(self.documents)} policies.")
        except Exception as e:
            logger.error(f"❌ Error adding to ChromaDB: {str(e)}")

    def retrieve_policy(self, query, top_k=3, similarity_threshold=0.8):
        """Retrieves relevant policies based on user query."""
        try:
            query_embedding_response = self.openai_client.embeddings.create(
                input=[query],
                model="text-embedding-ada-002"
            )

            query_embedding = query_embedding_response.data[0].embedding

            results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)

            retrieved_docs = results.get("documents", [[]])[0]
            similarities = results.get("distances", [[]])[0]

            filtered_docs = [doc for doc, similarity in zip(retrieved_docs, similarities) if similarity >= similarity_threshold]

            if not filtered_docs:
                logger.warning("❌ No relevant policy found (below threshold).")
                return ["No relevant policy found."]

            logger.info(f"✅ Retrieved {len(filtered_docs)} policies above threshold.")
            return filtered_docs
        except Exception as e:
            logger.error(f"❌ Error retrieving from ChromaDB: {str(e)}")
            return ["Error retrieving policy."]