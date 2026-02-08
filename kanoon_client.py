import requests
import config

class KanoonClient:
    def __init__(self):
        self.base_url = config.BASE_URL
        self.headers = {
            "Authorization": f"Token {config.API_TOKEN}",
            "Accept": "application/json"
        }

    def search_documents(self, query):
        try:
            resp = requests.post(f"{self.base_url}/search/", headers=self.headers, params={"formInput": query})
            return resp.json() if resp.status_code == 200 else {}
        except:
            return {}

    def get_document(self, doc_id):
        try:
            resp = requests.post(f"{self.base_url}/doc/{doc_id}/", headers=self.headers)
            return resp.json() if resp.status_code == 200 else {}
        except:
            return {}