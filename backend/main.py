import os
os.environ["HF_HUB_DISABLE_SSL_VERIFICATION"] = "1"
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers.pipelines import pipeline
from rag.retriever import SimpleRetriever
from rag.wikipedia_retriever import WikipediaRetriever

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ChatbotPipeline = pipeline("text-generation", model="C:/Users/amad.mateen/Downloads/tinyllama")
Retriever = SimpleRetriever("rag/banking_faq.txt")
WikiRetriever = WikipediaRetriever()

class ChatRequest(BaseModel):
    UserMessage: str


class ChatResponse(BaseModel):
    BotMessage: str
    FAQContext: str = ""
    WikiContext: str = ""
    Status: str = ""


@app.post("/chat", response_model=ChatResponse)
async def ChatEndpoint(ChatData: ChatRequest):
    UserInput = ChatData.UserMessage
    BankingKeywords = [
    # Core Banking
    "account", "balance", "transaction", "deposit", "withdraw", "transfer", "statement", "branch", "bank",
    "atm", "credit", "debit", "card", "pin", "check", "cheque", "overdraft", "limit", "account number",
    "minimum balance", "account type", "savings account", "current account", "fixed deposit", 
    "recurring deposit", "passbook", "banking", "finance", "financial","economy"

    # Digital Banking & Payments
    "netbanking", "mobile banking", "online banking", "internet banking", "upi", "wallet", "payment", 
    "bill", "qr code", "auto debit", "scheduled payment", "transaction ID", "fund transfer", "neft",
    "rtgs", "imps", "iban", "swift", "ifsc", "virtual card", "contactless", "tokenization",

    # Loans & Credit
    "loan", "personal loan", "home loan", "car loan", "education loan", "gold loan", "mortgage", 
    "emi", "interest", "installment", "repayment", "prepayment", "foreclosure", "principal", 
    "amortization", "credit limit", "credit score", "credit report", "underwriting",

    # Security & Fraud
    "fraud", "phishing", "otp", "authentication", "2fa", "mfa", "encryption", "cybersecurity", 
    "secure login", "password", "unauthorized", "blocked", "suspicious", "security question",

    # Investment & Wealth
    "investment", "mutual fund", "stock", "bond", "equity", "debt", "portfolio", "dividend", 
    "returns", "sip", "nifty", "sensex", "brokerage", "demat", "trading", "ipo", "capital gain", 
    "nps", "pension", "etf", "commodities", "derivatives", "forex", "currency", "exchange rate",

    # Insurance & Risk
    "insurance", "premium", "life insurance", "health insurance", "policy", "claim", "coverage", 
    "maturity", "nominee", "term plan", "risk", "actuary", "deductible",

    # General Financial Terms
    "rewards", "cashback", "fees", "charges", "service fee", "tax", "gst", "income", "expense",
    "budget", "audit", "ledger", "invoice", "billing", "reconciliation", "fiscal", "roi", "apy", 
    "financial year", "statement period", "due date", "arrears", "subsidy", "voucher", "subvention"
]

    if not any(word in UserInput.lower() for word in BankingKeywords):
        return ChatResponse(BotMessage="I'm designed to assist with banking and financial questions only. I'm unable to help with that.", Status="Not banking related")

    # Status: retrieving FAQ
    status = "Retrieving FAQ..."
    retrieved = Retriever.retrieve(UserInput, top_k=1)
    faq_context = ""
    if retrieved:
        faq_context = f"Q: {retrieved[0][0]}\nA: {retrieved[0][1]}\n"

    # Status: retrieving Wikipedia
    status = "Retrieving Wikipedia..."
    wiki_context = WikiRetriever.retrieve(UserInput, sentences=2)

    # Status: bot is typing
    status = "Bot is typing..."
    context = faq_context + wiki_context + "\n"
    Prompt = f"<|system|>\nYou are a helpful assistant.\n{context}<|user|>\n{UserInput}\n<|assistant|>\n"
    Result = ChatbotPipeline(Prompt, max_length=512, num_return_sequences=1, truncation=True)
    BotReply = Result[0]["generated_text"].split("<|assistant|>")[-1].strisp()
    return ChatResponse(BotMessage=BotReply, Status=status)
