from langchain_astradb import AstraDBVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_core.documents import Document

import os
import sys
import pandas as pd
from typing import List
from config.config_loader import load_config
from utils.model_loader import ModelLoader

# Load .env file and update system path
load_dotenv('E:\\customer_support_agnet\\.env')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["ASTRA_DB_API_ENDPOINT"] = os.getenv("ASTRA_DB_API_ENDPOINT")
os.environ["ASTRA_DB_APPLICATION_TOKEN"] = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
os.environ["ASTRA_DB_KEYSPACE"] = os.getenv("ASTRA_DB_KEYSPACE")


class DataIngestion:
    def __init__(self):
        """
        Initialize DataIngestion pipeline: environment, models, CSV path, and configs.
        """
        print("Initializing DataIngestion pipeline...")
        self.model_loader = ModelLoader()
        self._load_env_variables()
        self.csv_path = self._get_csv_path()
        self.product_data = self._load_csv()
        self.config = load_config()

    def _load_env_variables(self):
        """
        Validate and load environment variables.
        """
        required_vars = [
            "GOOGLE_API_KEY",
            "ASTRA_DB_API_ENDPOINT",
            "ASTRA_DB_APPLICATION_TOKEN",
            "ASTRA_DB_KEYSPACE"
        ]
        missing_vars = [var for var in required_vars if os.getenv(var) is None]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")

        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.db_api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
        self.db_application_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        self.db_keyspace = os.getenv("ASTRA_DB_KEYSPACE")

    def _get_csv_path(self):
        """
        Returns the path to the product review CSV file.
        """
        current_dir = os.getcwd()
        csv_path = os.path.join(current_dir, 'data', 'amazon_product_review.csv')
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")
        return csv_path

    def _load_csv(self):
        """
        Loads product data from the CSV file into a DataFrame.
        """
        df = pd.read_csv(self.csv_path)
        expected_columns = {'product_title', 'rating', 'summary', 'review'}

        if not expected_columns.issubset(set(df.columns)):
            raise ValueError(f"CSV must contain columns: {expected_columns}")

        return df

    def transform_data(self) -> List[Document]:
        """
        Transforms product data into a list of LangChain Document objects.
        """
        documents = []

        for _, row in self.product_data.iterrows():
            metadata = {
                "product_name": row['product_title'],
                "product_rating": row['rating'],
                "product_summary": row['summary']
            }
            doc = Document(page_content=row['review'], metadata=metadata)
            documents.append(doc)

        return documents

    def store_in_vector_db(self, documents: List[Document]):
        """
        Stores documents into AstraDB vector store.
        """
        collection_name = self.config['astra_db']['collection_name']

        vstore = AstraDBVectorStore(
            embedding=self.model_loader.load_embeddings(),
            collection_name=collection_name,
            api_endpoint=self.db_api_endpoint,
            token=self.db_application_token,
            namespace=self.db_keyspace
        )

        inserted_ids = vstore.add_documents(documents)
        return vstore, inserted_ids

    def run_pipeline(self):
        """
        Run the full data ingestion pipeline: transform and store.
        """
        documents = self.transform_data()
        vstore, inserted_ids = self.store_in_vector_db(documents)

        query = "Can you tell me the low budget headphone?"
        results = vstore.similarity_search(query)

        print(f"\nSample search results for query: '{query}'")
        for res in results:
            print(f"Content: {res.page_content}\nMetadata: {res.metadata}\n")


# if __name__ == "__main__":
#     ingestion = DataIngestion()
#     ingestion.run_pipeline()
