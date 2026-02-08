import requests
import config

class KanoonClient:
    def __init__(self):
        self.base_url = config.BASE_URL
        self.headers = {
            "Authorization": f"Token {config.API_TOKEN}",
            "Accept": "application/json"
        }

    def search_documents(self, query, pagenum=0):
        """
        Searches for documents based on a query with pagination support.
        """
        endpoint = f"{self.base_url}/search/"
        params = {
            "formInput": query,
            "pagenum": pagenum
        }
        
        try:
            # The API documentation specifies parameters in the URL, but POST is also supported for the API key approach.
            # Using params=params ensures they are added to the URL query string.
            response = requests.post(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching documents: {e}")
            return {}

    def get_document(self, doc_id):
        endpoint = f"{self.base_url}/doc/{doc_id}/"
        try:
            response = requests.post(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching document {doc_id}: {e}")
            return {}