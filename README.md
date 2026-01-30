# AI_powered-chatbot-for-customer-service
# 🤖 SupportMate — AI Customer Support Chatbot (RAG + NLP)

SupportMate is an AI-powered customer support chatbot built using NLP and Retrieval-Augmented Generation (RAG).  
It answers user queries about orders, shipping, refunds, and store policies by combining a knowledge base, vector search, and a local language model.

The system also connects to a database to fetch real order information in real time.

---

## 🚀 Features

- ✅ RAG pipeline with FAISS vector search
- ✅ Semantic document retrieval using Sentence Transformers
- ✅ Local LLM reasoning (Qwen 2.5)
- ✅ Query interpretation using FLAN-T5
- ✅ MySQL order lookup integration
- ✅ Streamlit chat UI
- ✅ Knowledge base built from documents
- ✅ Source chunk inspection for transparency
- ✅ CLI chatbot mode

---

## 🧠 Architecture

User Question  
→ Query Interpreter  
→ Vector Search (FAISS)  
→ Retrieved Context  
→ LLM Reasoner  
→ Final Response

If an order number is detected → database lookup is triggered instead of LLM guessing.

---

## 📂 Project Structure

```
project/
│
├── app.py                # Streamlit UI :contentReference[oaicite:0]{index=0}
├── chatbot.py            # Main RAG pipeline :contentReference[oaicite:1]{index=1}
├── rag_search.py         # FAISS retrieval :contentReference[oaicite:2]{index=2}
├── slm_reasoner.py       # Local LLM reasoning :contentReference[oaicite:3]{index=3}
├── slm_interpreter.py    # Query classification :contentReference[oaicite:4]{index=4}
├── db.py                 # MySQL database connector :contentReference[oaicite:5]{index=5}
├── main.py               # CLI chatbot mode :contentReference[oaicite:6]{index=6}
├── build_kb_index.py     # FAISS index builder :contentReference[oaicite:7]{index=7}
├── build_kb_docs.py      # Document → KB converter :contentReference[oaicite:8]{index=8}
│
├── kb_v2/                # Knowledge base text files
├── raw_docs/             # Source documents (PDF/DOCX/HTML)
└── README.md
```

---

Required libraries include:

- transformers
- sentence-transformers
- faiss-cpu
- torch
- streamlit
- mysql-connector-python
- numpy

---

## 📚 Build Knowledge Base

Convert documents into KB text:

```
python build_kb_docs.py
```

Build FAISS index:

```
python build_kb_index.py
```

---

## 🗄 Database Setup

Edit credentials in `db.py`:

```python
host="localhost"
user="your_user"
password="your_password"
database="retail"
```

Expected schema:

```
orders(order_id, status, delivery_status, last_known_location)
```

---

## ▶️ Run the Chatbot

### Streamlit Web UI

```
streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

### Terminal Chat Mode

```
python main.py
```

---

## 💬 Example Queries

- "Where is my order 12345?"
- "What is your return policy?"
- "How long does shipping take?"
- "I want a refund"

---

## 🔍 Transparency Mode

Enable **“Show retrieved context”** in sidebar to inspect KB chunks used to generate the answer.

---

## 🎯 Use Cases

- Customer support automation
- Retail helpdesk chatbot
- Policy & FAQ assistant
- Order tracking system
- Internal knowledge base assistant

---

## 🧪 Future Improvements

- Cloud deployment (AWS/Azure)
- Conversation memory
- Voice interface
- Multi-language support
- Authentication layer
- Admin dashboard

---

## 👨‍💻 Author

Suraj Joshi  
AI / NLP / Data Enthusiast


