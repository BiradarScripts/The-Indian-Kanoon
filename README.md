Here is a comprehensive and professional `README.md` file for your repository. You can copy the code block below and save it as `README.md` in your project root.


# 🇮🇳 Indian Kanoon PII Masker

A robust Python-based tool that interfaces with the **Indian Kanoon API** to fetch legal documents and automatically masks **Personally Identifiable Information (PII)** (such as names, phone numbers, emails, and addresses) using advanced Natural Language Processing (NLP).

This project is designed for legal tech developers, researchers, and data privacy advocates who need to process legal texts while maintaining individual privacy.

---

## 🚀 Features

* **API Integration**: Seamlessly connects to the Indian Kanoon API using token-based authentication.
* **Smart Search**: Allows searching for legal documents by keyword, case type, or query directly from the command line.
* **NLP-Powered Masking**: Utilizes **Microsoft Presidio** and **spaCy** to intelligently identify and redact sensitive entities.
* **Context-Aware Redaction**: Distinguishes between general text and specific entities like:
    * `[REDACTED_PERSON]` - Names of individuals
    * `[REDACTED_PHONE_NUMBER]` - Mobile and landline numbers
    * `[REDACTED_EMAIL]` - Email addresses
    * `[REDACTED_LOCATION]` - Physical addresses and cities
    * `[REDACTED_PAN]` - Permanent Account Numbers
* **Modular Design**: Clean separation of concerns between API handling (`kanoon_client.py`), masking logic (`masking_engine.py`), and execution (`main.py`).

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following:

1.  **Python 3.8+** installed on your system.
2.  An active **Indian Kanoon API Token**.
    * *If you don't have one, register at [Indian Kanoon API](https://api.indiankanoon.org/).*

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/indian-kanoon-pii-masker.git](https://github.com/yourusername/indian-kanoon-pii-masker.git)
cd indian-kanoon-pii-masker

```

### 2. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt

```

> **Note:** If `requirements.txt` is missing, you can install the core packages manually:
> `pip install requests presidio-analyzer presidio-anonymizer spacy`

### 3. Download NLP Model

The masking engine requires a trained English language model from spaCy to understand the context of the text. Run this command in your terminal:

```bash
python -m spacy download en_core_web_lg

```

*(We recommend `en_core_web_lg` (large) for better accuracy over the smaller models.)*

---

## ⚙️ Configuration

1. Open the `config.py` file in your code editor.
2. Replace the placeholder text with your actual Indian Kanoon API token.

```python
# config.py

# Your Indian Kanoon API Token
API_TOKEN = "YOUR_ACTUAL_TOKEN_HERE" 

# Base URL for Indian Kanoon API
BASE_URL = "[https://api.indiankanoon.org](https://api.indiankanoon.org)"

```

**⚠️ Security Warning:** Never commit your `config.py` with the real API token to public repositories (GitHub/GitLab). Add `config.py` to your `.gitignore` file.

---

## 🏃‍♂️ Usage

To run the full pipeline (Search -> Fetch -> Mask -> Save), simply execute the `main.py` script:

```bash
python main.py

```

### How it works:

1. The script initializes the API client and the NLP Masking Engine.
2. It sends a search query (default: `"contract breach"`) to Indian Kanoon.
3. It retrieves the first document from the search results.
4. It downloads the full text of that document.
5. It runs the text through the PII Masker.
6. Finally, it saves the masked document as an HTML file (e.g., `masked_doc_12345.html`).

---

## 📂 Project Structure

```text
indian-kanoon-pii-masker/
│
├── config.py           # Stores API credentials and constants
├── kanoon_client.py    # Handles all network requests to Indian Kanoon API
├── masking_engine.py   # NLP logic using Presidio & Spacy for PII detection
├── main.py             # Entry point: Orchestrates the search and mask workflow
├── requirements.txt    # List of python dependencies
└── README.md           # Project documentation

```

---

## 🧩 Customization

You can customize which entities are masked by modifying `masking_engine.py`.

**To add or remove entities:**
Locate the `self.analyzer.analyze` call and update the `entities` list:

```python
results = self.analyzer.analyze(
    text=text,
    entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION", "IN_PAN", "DATE_TIME"], # Added DATE_TIME
    language='en'
)

```

**Supported Entities:**

* `PERSON`
* `PHONE_NUMBER`
* `EMAIL_ADDRESS`
* `IN_AADHAAR` (Indian Aadhaar numbers)
* `IN_PAN` (Indian PAN card numbers)
* `LOCATION`
* `DATE_TIME`
* ...and more.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

---

## 🙏 Acknowledgments

* **Indian Kanoon** for providing the API and vast legal database.
* **Microsoft Presidio** for the excellent PII anonymization framework.
* **spaCy** for the industrial-strength NLP models.

```

### Next Step
Would you like me to also provide a `.gitignore` file to ensure you don't accidentally upload your API key to GitHub?

```
