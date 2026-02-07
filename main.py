from kanoon_client import KanoonClient
from masking_engine import PIIMasker
import json
import os

def run_pipeline():
    client = KanoonClient()
    masker = PIIMasker()
    
    search_query = "contract breach"
    print(f"Searching for: {search_query}...")
    
    search_results = client.search_documents(search_query)
    
    if not search_results or 'docs' not in search_results:
        print("No results found or authentication failed.")
        return

    first_doc = search_results['docs'][0]
    doc_id = first_doc['tid']
    doc_title = first_doc['title']
    
    print(f"Processing Document ID: {doc_id} | Title: {doc_title}")
    
    full_doc_data = client.get_document(doc_id)
    
    if full_doc_data and 'doc' in full_doc_data:
        original_text = full_doc_data['doc']
        
        print("Masking PII (this may take a moment)...")
        masked_text = masker.mask_text(original_text)
        
        output_filename = f"masked_doc_{doc_id}.html"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(masked_text)
            
        print(f"Success! Masked document saved to: {output_filename}")
        

    else:
        print("Failed to retrieve document content.")

if __name__ == "__main__":
    run_pipeline()