# 🇮🇳 Indian Kanoon : Context-Aware PII Masker

A sophisticated Python-based tool that interfaces with the **Indian Kanoon API** to fetch legal documents and intelligently masks sensitive information. 

Unlike standard maskers that hide *everyone*, this tool uses **Context-Aware NLP** to specifically protect **Victims and their Families** while keeping Judges, Lawyers, and the Accused visible for legal context. It features a modern **Web Interface** for easy searching and side-by-side comparison.

---

## 🚀 Features

* **Context-Aware Protection**: Uses logic to distinguish between public figures (Judges, Lawyers) and vulnerable individuals (Victims, Family).
    * *Masks:* "Sita (Victim)", "Raju (Son of...)" -> `[VICTIM/FAMILY]`
    * *Keeps:* "Justice Sharma", "Advocate Mehta" -> Visible
* **Smart Search UI**: A clean, browser-based interface to search the Indian Kanoon database.
* **Side-by-Side Comparison**: Instantly view the original legal text next to the safe, masked version.
* **Standard PII Redaction**: Automatically hides:
    * `[PHONE]` - Mobile and landline numbers
    * `[EMAIL]` - Email addresses
    * `[LOC]` - Physical addresses
* **Powered by**: FastAPI (Web), Microsoft Presidio (PII), and spaCy (NLP).

---

## 🛠️ Prerequisites

1.  **Python 3.8+** installed on your system.
2.  An active **Indian Kanoon API Token**.
    * *Get one at [Indian Kanoon API](https://api.indiankanoon.org/).*

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/indian-kanoon-safeview.git](https://github.com/yourusername/indian-kanoon-safeview.git)
cd indian-kanoon-safeview

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Download NLP Model

The context engine requires a robust English model to understand relationships in text.

```bash
python -m spacy download en_core_web_lg

```

*(Note: This download is approx 800MB. If it times out, try running it again.)*

---

## ⚙️ Configuration

1. Open `config.py` in your code editor.
2. Add your API token:

```python
# config.py
API_TOKEN = "YOUR_ACTUAL_TOKEN_HERE" 
BASE_URL = "[https://api.indiankanoon.org](https://api.indiankanoon.org)"

```

**⚠️ Security Warning:** Add `config.py` to your `.gitignore` file to prevent leaking your API key.

---

## 🏃‍♂️ Usage

This project runs as a local web server.

### 1. Start the Server

Run the following command in your terminal:

```bash
uvicorn app:app --reload

```

### 2. Open the Interface

Open your web browser and navigate to:
👉 **https://www.google.com/search?q=http://127.0.0.1:8000**

### 3. How to Use

1. Enter a search term (e.g., *"dowry harassment"*, *"cyber crime"*).
2. Click **Search** to fetch real cases from Indian Kanoon.
3. Click on any document title from the results.
4. View the **Split-Screen Mode**:
* **Left**: Original Document
* **Right**: Safe Document (Victims & Family masked)



---

## 📂 Project Structure

```text
indian-kanoon-safeview/
│
├── app.py              # 🚀 The Web Server (FastAPI) & Routes
├── kanoon_client.py    # 🔌 Connects to Indian Kanoon API
├── masking_engine.py   # 🧠 The "Smart" Logic (Context-Aware Filtering)
├── config.py           # 🔑 API Credentials
├── requirements.txt    # 📦 Python Dependencies
├── README.md           # 📄 This file
└── templates/
    └── index.html      # 🎨 The User Interface (HTML/CSS)

```

---

## 🧠 How the Logic Works

The `masking_engine.py` does not just blindly mask every name. It follows this logic:

1. **Entity Detection**: Finds all People, Phones, Emails, and Locations.
2. **Context Check**: For every person found, it checks the surrounding words (50 characters before/after).
3. **Keyword Matching**: It looks for sensitive triggers like:
* *"victim", "deceased", "minor", "survivor"*
* *"wife of", "son of", "daughter of"*


4. **Decision**:
* If a trigger is found → **MASK** as `[VICTIM/FAMILY]`
* If no trigger is found → **KEEP** (Likely a Judge, Lawyer, or Accused)


5. **Always Mask**: Phone numbers, Emails, and Addresses are always masked for safety.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

* **Indian Kanoon** for the API.
* **Microsoft Presidio** for the PII framework.
* **FastAPI** for the high-performance web framework.

```

```
