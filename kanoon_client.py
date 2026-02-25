import os
import requests
from dotenv import load_dotenv

load_dotenv()  

class KanoonClient:
    def __init__(self, api_token: str | None = None, base_url: str | None = None, timeout: int = 30):
        self.base_url = (base_url or os.getenv("BASE_URL", "https://api.indiankanoon.org")).rstrip("/")
        self.api_token = api_token or os.getenv("API_TOKEN")

        if not self.api_token:
            raise ValueError("Missing API_TOKEN. Set it in .env or environment variables.")

        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {self.api_token}",
            "Accept": "application/json",
        })

    def search_documents(self, query: str, pagenum: int = 0) -> dict:
        """
        Searches for documents based on a query with pagination support.
        """
        endpoint = f"{self.base_url}/search/"
        params = {"formInput": query, "pagenum": pagenum}

        try:
            # Keep POST (as you had), but set a timeout and reuse a session.
            r = self.session.post(endpoint, params=params, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching documents: {e}")
            return {}

    def get_document(self, doc_id: str) -> dict:
        """
        Fetches a document by ID.
        """
        endpoint = f"{self.base_url}/doc/{doc_id}/"

        try:
            r = self.session.post(endpoint, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching document {doc_id}: {e}")
            return {}