# Banking Chatbot API

A FastAPI-based backend for a banking and finance-focused chatbot. Combines local LLM text generation, FAQ retrieval, and Wikipedia context to answer user questions about banking, finance, and related topics.

## Features
- Accepts user questions via `/chat` endpoint (POST)
- Uses a local LLM (TinyLlama) for text generation
- Retrieves relevant FAQ answers from a text file
- Retrieves Wikipedia context for additional information
- Filters out non-banking/finance questions
- CORS enabled for frontend integration

## How It Works
- User sends a message to `/chat` (JSON: `{ "UserMessage": "..." }`)
- If the message is banking/finance related, the bot:
  - Retrieves FAQ context using semantic search
  - Retrieves Wikipedia context for the query
  - Generates a response using the LLM, including both contexts
- Returns a JSON response with bot reply, FAQ context, Wikipedia context, and status

## Requirements
- Python 3.8+
- FastAPI
- transformers
- rag (custom retriever modules)
- uvicorn
- A local HuggingFace-compatible LLM (e.g., TinyLlama)
- `rag/banking_faq.txt` (FAQ file)

Install dependencies:
```bash
pip install fastapi transformers uvicorn
```

## Usage
1. Start the API server:
    ```bash
    uvicorn backend.main:app --reload --port 8000
    ```
2. Send POST requests to `/chat` with JSON body:
    ```json
    { "UserMessage": "How do I open a savings account?" }
    ```
3. Response example:
    ```json
    {
      "BotMessage": "...",
      "FAQContext": "...",
      "WikiContext": "...",
      "Status": "..."
    }
    ```

## File Structure
- `backend/main.py`: FastAPI app and chatbot logic
- `backend/rag/retriever.py`: FAQ retriever
- `backend/rag/wikipedia_retriever.py`: Wikipedia retriever
- `backend/requirements.txt`: Python dependencies
- `backend/rag/banking_faq.txt`: FAQ data file

## Notes
- The chatbot only responds to banking/finance-related queries
- Requires a local LLM model path (update in `main.py` if needed)
- FAQ and Wikipedia context are included in bot responses
- CORS is enabled for frontend integration

## License
MIT

## Author
amad-mateen
