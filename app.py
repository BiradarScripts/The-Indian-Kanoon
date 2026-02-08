from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from kanoon_client import KanoonClient
from masking_engine import SmartMasker
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = KanoonClient()
masker = SmartMasker()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "pagenum": 0})

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...), pagenum: int = Form(0)):
    # Fetch results for the specific page
    results = client.search_documents(query, pagenum=pagenum)
    docs = results.get('docs', [])
    
    # Calculate if we should show a "Next" button
    # (Indian Kanoon usually returns 10 results per page)
    has_next = len(docs) >= 10

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "docs": docs, 
        "query": query,
        "pagenum": pagenum,
        "has_next": has_next
    })

@app.get("/process/{doc_id}", response_class=HTMLResponse)
async def process_doc(request: Request, doc_id: int):
    raw_data = client.get_document(doc_id)
    original_text = raw_data.get('doc', 'Error fetching document')
    title = raw_data.get('title', 'Unknown Title')

    # Apply the context-aware masking
    masked_text = masker.mask_victims_and_family(original_text)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "doc_id": doc_id,
        "title": title,
        "original_text": original_text,
        "masked_text": masked_text,
        "view_mode": "compare"
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)