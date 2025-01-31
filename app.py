import gradio as gr
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_community.llms import Ollama

llm = Ollama(model="mistral")  # Keep Ollama server running!


def load_document(file_path):
    """Load the PDF or DOCX document, raise ValueError if unsupported format."""
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")
    
    try:
        return loader.load()
    except Exception as e:
        raise RuntimeError(f"Document load failed: {str(e)}")


def process_and_classify(file):
    """Process the document and return:
       1. State (with 'text' and 'doc_type'),
       2. Error box update (hidden if success, visible if error).
    """

    if not file:
        return (
            None,
            gr.update(visible=True, value="No file uploaded.")
        )
        
    try:
        docs = load_document(file.name)
        full_text = "\n".join([doc.page_content for doc in docs])
        
        # Classification prompt
        classification_prompt = f"""
        Identify the document type in 1-2 words. Examples:
        - Invoice
        - Contract
        - KYC Form
        - Loan Document
        - Credit Card Bill
        - Insurance Policy
        
        Return ONLY the exact document type name. Do not explain.
        Document excerpt: {full_text[:1500]}
        """
        
        doc_type = llm.invoke(classification_prompt).strip()

         # Summary Generation
        summary_prompt = f"""
        Generate a concise 3-5 bullet point summary of this document.
        Focus on key entities, amounts, dates, and parties involved.
        Use markdown formatting with bullet points.
        Keep each point under 15 words.
        
        Document text: {full_text[:3000]}
        """
        summary = llm.invoke(summary_prompt).strip()
        
        return (
            {"text": full_text, "doc_type": doc_type, "summary": summary},
            gr.update(visible=False, value="")
        )
        
    except Exception as e:
        # Show error box on failure
        return (
            None,
            gr.update(visible=True, value=f"Error: {str(e)}")
        )


def answer_question(question, state):
    """Perform Q&A with state validation."""
    if not state or "text" not in state:
        return "Upload a document first."
    
    try:
        response = llm.invoke(
            f"Answer this question based strictly on the document text: {question}\n\n"
            f"Document excerpt: {state['text'][:3000]}\n"
            "If the answer isn't in the document, say 'Not found in document'."
        )
        return response.strip()
    except Exception as e:
        return f"Error generating answer: {str(e)}"


def hide_error_box(_=None):
    """Helper function to reset/hide the error box."""
    return gr.update(visible=False, value="")


with gr.Blocks() as app:
    state = gr.State()  # Holds {"text": "...", "doc_type": "..."}
    
    error_box = gr.Textbox(
        label="Error",
        visible=False,
        interactive=False
    )

    gr.Markdown("# Document Parser with Document Type Detection & Q&A")
    
    with gr.Row():
        file_input = gr.File(label="Upload Document (PDF/DOCX)")
    
    with gr.Row():
        doc_type = gr.Textbox(label="Document Type", interactive=False)
        summary = gr.Markdown(label="Document Summary")
    
    with gr.Row():
        question = gr.Textbox(label="Ask a Question")
    
    with gr.Row():
        answer = gr.Textbox(label="Answer", interactive=False)
    
    # Chain of events when a new file is uploaded:
    # 1) Immediately hide the error box
    # 2) Then process_and_classify
    # 3) Then extract the document type for display
    file_input.change(
        fn=hide_error_box,
        inputs=[],
        outputs=error_box
    ).then(
        fn=process_and_classify,
        inputs=file_input,
        outputs=[state, error_box]
    ).then(
        fn=lambda s: s["doc_type"] if s else "",
        inputs=state,
        outputs=doc_type
    ).then(
        lambda s: s["summary"] if s else "",
        inputs=state,
        outputs=summary
    )

    # Handle question submit for Q&A
    question.submit(
        fn=answer_question,
        inputs=[question, state],
        outputs=answer
    )

if __name__ == "__main__":
    app.launch()
