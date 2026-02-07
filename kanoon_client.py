import requests
import config

class KanoonClient:
    def __init__(self):
        self.base_url = config.BASE_URL
        self.headers = {
            "Authorization": f"Token {config.API_TOKEN}",
            "Accept": "application/json"  # We request JSON as per docs
        }

    def search_documents(self, query, pagenum=0):
        """
        Searches for documents based on a query.
        """
        endpoint = f"{self.base_url}/search/"
        params = {
            "formInput": query,
            "pagenum": pagenum
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching documents: {e}")
            return None

    def get_document(self, doc_id):
        """
        Fetches the full text of a specific document by DocID.
        """
        # as per docs: https://api.indiankanoon.org/doc/<docid>/
        endpoint = f"{self.base_url}/doc/{doc_id}/"
        
        try:
            response = requests.post(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching document {doc_id}: {e}")
            return None