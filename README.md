# Document Parser with Summary & Q&A

A Python-based application that uses Ollama and LangChain to analyze uploaded documents (PDF/DOCX), detect their type, generate summaries, and answer questions based on the content.

## Features ✨

- **Document Type Detection**: Automatically identifies document type (e.g., Invoice, Contract, KYC Form).
- **Document Summary**: Generates a concise 3-5 bullet point summary of the document.
- **Q&A**: Ask questions and get answers based on the document content.
- **Modern UI**: Clean and intuitive Gradio interface.
- **Local LLM**: Powered by Ollama's Mistral model for privacy and offline use.

## Prerequisites 📋

- Python 3.8+
- Ollama (for running Mistral locally)
- Git (optional, for cloning the repository)

## Installation 🛠️

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/document-parser.git
cd document-parser
```

### 2. Set Up Virtual Environment

#### Linux/Mac:

```bash
python -m venv venv
source venv/bin/activate
```

#### Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

#### Mac/Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows:

```bash
winget install ollama.ollama
```

### 5. Download Mistral Model

```bash
ollama pull mistral
```

## Running the Application 🚀

### 1. Start Ollama Server (in a separate terminal):

```bash
ollama serve
```

### 2. Run the Application:

```bash
python app.py
```

### 3. Access the UI:

Open your browser and navigate to:

```
http://localhost:7860
```

## Usage 🖥️

### Upload a Document:

- Supported formats: PDF, DOCX.
- The app will automatically detect the document type and generate a summary.

### Ask Questions:

- Type your question in the "Ask a Question" box.
- The app will provide answers based on the document content.

## Example Workflow

### Upload an `invoice.pdf`:

**Document Type**: Invoice  
**Summary**:

```markdown
- Invoice dated 2023-10-15 for $1,500
- Customer: ABC Corporation (ID: AC-123)
- Payment due by 2023-11-01
- Services: Cloud hosting and maintenance
```

**Question**: "What is the invoice number?"  
**Answer**: "The invoice number is INV-2023-001."

## Contributing 🤝

Contributions are welcome! Please open an issue or submit a pull request.
